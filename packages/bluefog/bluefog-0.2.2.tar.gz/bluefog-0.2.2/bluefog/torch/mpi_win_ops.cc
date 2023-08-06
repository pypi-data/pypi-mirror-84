// Copyright 2020 Bluefog Team. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// ==============================================================================

#include "mpi_win_ops.h"

#include <torch/extension.h>
#include <torch/torch.h>

#include <chrono>
#include <cstdlib>
#include <memory>
#include <thread>

#include "../common/cuda_util.h"
#include "../common/logging.h"
#include "../common/operations.h"
#include "../common/timeline.h"
#include "adapter.h"
#include "handle_manager.h"

namespace bluefog {
namespace torch {

using ::bluefog::common::bluefog_load_topology;
using ::bluefog::common::bluefog_load_topology_weights;
using ::bluefog::common::bluefog_neighbor_size;
using ::bluefog::common::with_device;
using ::bluefog::common::EnqueueTensorWindowAccumulate;
using ::bluefog::common::EnqueueTensorWindowGet;
using ::bluefog::common::EnqueueTensorWindowPut;
using ::bluefog::common::GetBluefogTimeline;
using ::bluefog::common::Status;
using ::bluefog::common::Timeline;
using NeighborTable = std::unordered_map<int, std::shared_ptr<TorchTensor>>;

// static here means Local/private variable.
static HandleManager win_handle_manager;
static WinTorchStorageManager win_storage_manager;

static const char* BLUEFOG_WIN_ON_GPU = std::getenv("BLUEFOG_WIN_ON_GPU");
static const bool WIN_ON_CPU =
    !((BLUEFOG_WIN_ON_GPU != nullptr) && (*BLUEFOG_WIN_ON_GPU == '1'));

namespace {

int GetDeviceID(const ::torch::Tensor& tensor) {
  if (tensor.device().is_cuda()) {
    return tensor.device().index();
  }
  return CPU_DEVICE_ID;
}

double GetWinAssociatedP(const std::string& name) {
  ThrowIfError(common::CheckInitialized());
  double weight = 0.0;
  Status status = common::GetWinAssociatedPByNameAndRank(
      name, common::bluefog_rank(), &weight);
  ThrowIfError(status);
  return weight;
}

void SetWinAssociatedP(const std::string& name, const double value) {
  ThrowIfError(common::CheckInitialized());
  Status status = common::SetWinAssociatedPByNameAndRank(
      name, common::bluefog_rank(), value);
  ThrowIfError(status);
}

}  // namespace

bool WinTorchStorageManager::RegisterWinName(
    const std::string& name, const int device,
    std::shared_ptr<TorchTensor> tensor, const bool zero_init) {
  if (tensors_map_.find(name) != tensors_map_.end()) {
    return false;
  }
  int* sources_ptr = nullptr;
  int* destinations_ptr = nullptr;
  bluefog_load_topology(&in_neighbor_degree_, sources_ptr,
                        &out_neighbor_degree_, destinations_ptr);
  // We need to allocate neighbor_indegree tensor space for it.
  NeighborTable neighbor_tensors;
  for (int i = 0; i < in_neighbor_degree_; i++) {
    std::shared_ptr<TorchTensor> t = tensor->MakeCopy(device);
    if (zero_init) t->GetUnderlyingTensor().fill_(0.0);
    int source_rank = *(sources_ptr + i);
    neighbor_tensors[source_rank] = t;
  }
  tensors_map_[name] = neighbor_tensors;
  self_tensor_map_[name] = tensor;
  device_map_[name] = device;
  return true;
}

bool WinTorchStorageManager::UnregisterWinName(const std::string& name) {
  auto it = tensors_map_.find(name);
  if (it == tensors_map_.end()) {
    return false;
  }
  tensors_map_.erase(it);
  self_tensor_map_.erase(self_tensor_map_.find(name));
  device_map_.erase(device_map_.find(name));
  return true;
}

void WinTorchStorageManager::ClearAll() {
  tensors_map_.clear();
  self_tensor_map_.clear();
}

bool WinTorchStorageManager::GetStorageByname(
    const std::string& name,
    std::vector<std::shared_ptr<common::Tensor>>& tensors) {
  auto it = tensors_map_.find(name);
  if (it == tensors_map_.end()) {
    return false;
  }
  std::unordered_map<int, std::shared_ptr<TorchTensor>> neighbor_map =
      it->second;
  int* sources_ptr = nullptr;
  int* destinations_ptr = nullptr;
  bluefog_load_topology(&in_neighbor_degree_, sources_ptr,
                        &out_neighbor_degree_, destinations_ptr);

  // We have to insert it in order.
  for (int i = 0; i < in_neighbor_degree_; i++) {
    int source_rank = *(sources_ptr + i);
    tensors.emplace_back(neighbor_map[source_rank]);
  }
  return true;
}

bool WinTorchStorageManager::GetDeviceByName(const std::string& name,
                                             int* device) {
  auto it = device_map_.find(name);
  if (it == device_map_.end()) {
    return false;
  }
  *device = it->second;
  return true;
}

bool WinTorchStorageManager::GetStorageByNameRank(
    const std::string& name, const int rank,
    std::shared_ptr<TorchTensor>& tensor) {
  auto it = tensors_map_.find(name);
  if (it == tensors_map_.end()) {
    BFLOG(ERROR) << "Cannot find " << name << " in neighbor tensor map";
    return false;
  }
  std::unordered_map<int, std::shared_ptr<TorchTensor>> neighbor_map =
      it->second;
  auto it2 = neighbor_map.find(rank);
  if (it2 == neighbor_map.end()) {
    BFLOG(ERROR) << "Cannot find rank " << rank << " in " << name
                 << "neighbor tensor map";
    return false;
  }
  tensor = it2->second;
  return true;
}

bool WinTorchStorageManager::SetSelfStorageByName(
    const std::string& name, const ::torch::Tensor& tensor) {
  auto it = self_tensor_map_.find(name);
  if (it == self_tensor_map_.end()) {
    return false;
  }
  it->second->GetUnderlyingTensor().copy_(tensor);
  return true;
}

bool WinTorchStorageManager::SumWithNeighbor(const std::string& name,
                                             ::torch::Tensor local_tensor,
                                             bool associated_with_p) {
  auto it = tensors_map_.find(name);
  if (it == tensors_map_.end()) {
    return false;
  }
  for (auto& kv : it->second) {
    std::shared_ptr<TorchTensor> t = kv.second;
    local_tensor.add_(t->GetUnderlyingTensor());
  }
  if (associated_with_p) {
    double sum_p = GetWinAssociatedP(name);  // self value
    for (auto& kv : it->second) {
      int neighbor_rank = kv.first;
      double neighbor_p = 0.0;
      common::GetWinAssociatedPByNameAndRank(name, neighbor_rank, &neighbor_p);
      sum_p += neighbor_p;
    }
    SetWinAssociatedP(name, sum_p);
  }
  return true;
}

bool WinTorchStorageManager::AvgWithNeighbor(
    const std::string& name, ::torch::Tensor local_tensor, double self_weight,
    const std::unordered_map<int, double>& neighbor_weights,
    bool associated_with_p) {
  auto it = tensors_map_.find(name);
  if (it == tensors_map_.end()) {
    return false;
  }

  local_tensor.mul_(self_weight);

  auto neighbor_map = it->second;
  for (auto& kv : neighbor_weights) {
    double weight = kv.second;
    auto neighbor_tesnor = neighbor_map.at(kv.first)->GetUnderlyingTensor();
    local_tensor.add_(neighbor_tesnor.mul(weight));
  }
  if (associated_with_p) {
    double avg_p = GetWinAssociatedP(name) * self_weight;  // self value
    for (auto& kv : neighbor_weights) {
      int neighbor_rank = kv.first;
      double weight = kv.second;
      double associated_p = 0.0;
      common::GetWinAssociatedPByNameAndRank(name, neighbor_rank, &associated_p);
      avg_p += (associated_p * weight);
    }
    SetWinAssociatedP(name, avg_p);
  }
  return true;
}

bool WinTorchStorageManager::SumWithNeighbor(
    const std::string& name, ::torch::Tensor local_tensor,
    const std::vector<int>& source_ranks, bool associated_with_p) {
  if (tensors_map_.find(name) == tensors_map_.end()) {
    return false;
  }
  std::unordered_map<int, std::shared_ptr<TorchTensor>> neighbor_map =
      tensors_map_.at(name);
  for (int rank : source_ranks) {
    local_tensor.add_(neighbor_map.at(rank)->GetUnderlyingTensor());
  }
  if (associated_with_p) {
    double sum_p = GetWinAssociatedP(name);  // self value
    for (int neighbor_rank : source_ranks) {
      double neighbor_weight = 0.0;
      common::GetWinAssociatedPByNameAndRank(name, neighbor_rank,
                                             &neighbor_weight);
      sum_p += neighbor_weight;
    }
    SetWinAssociatedP(name, sum_p);
  }
  return true;
}

bool WinTorchStorageManager::AvgWithNeighbor(
    const std::string& name, ::torch::Tensor local_tensor,
    const std::vector<int>& source_ranks, bool associated_with_p) {
  if (!SumWithNeighbor(name, local_tensor, source_ranks, associated_with_p)) {
    return false;
  }
  // +1 here because source_ranks doesn't include self rank.
  double neighbor_cnt_with_self =
      static_cast<double>(source_ranks.size()) + 1.0;
  local_tensor.div_(neighbor_cnt_with_self);
  if (associated_with_p) {
    double self_associated_p = GetWinAssociatedP(name);
    SetWinAssociatedP(name, self_associated_p / neighbor_cnt_with_self);
  }
  return true;
}

void DoWinWait(int);

int DoWinCreate(::torch::Tensor tensor, const std::string& name,
                const bool zero_init) {
  ThrowIfError(common::CheckInitialized());

  auto device = GetDeviceID(tensor);
  std::shared_ptr<TorchTensor> bf_tensor;

  if (WIN_ON_CPU && tensor.device().is_cuda()) {
    ::torch::Tensor cpu_buffer =
        tensor.to(::torch::Device(::torch::kCPU), /*non_blocking=*/false);
    bf_tensor = std::make_shared<TorchTensor>(cpu_buffer);
    device = CPU_DEVICE_ID;
  } else {
    bf_tensor = std::make_shared<TorchTensor>(tensor);
  }

  // bf_neighbor_tensors is the vector with in-neighbor size and the order is
  // followed by neighbor order returned by bluefog_load_topology. 
  // It is assumed that the order is sorted ascendingly.
  std::vector<std::shared_ptr<common::Tensor>> bf_neighbor_tensors;

  if (!win_storage_manager.RegisterWinName(name, device, bf_tensor, zero_init)) return 0;
  if (!win_storage_manager.GetStorageByname(name, bf_neighbor_tensors))
    return 0;

  auto handle = win_handle_manager.AllocateHandle();
  auto enqueue_result =
      EnqueueTensorWindowCreate(bf_tensor, bf_neighbor_tensors, name, device,
                                [handle](const Status& status) {
                                  win_handle_manager.MarkDone(handle, status);
                                });

  ThrowIfError(enqueue_result);
  // Blocking ops. Wait until it is done.
  DoWinWait(handle);
  return 1;
}

namespace {

int ResetNeighborTensor(const std::string& name,
        const std::unordered_map<int, double>& neighbor_map, 
        bool associated_with_p) {
  std::shared_ptr<TorchTensor> bf_neighbor_tensor;
  for (auto& kv : neighbor_map) {
    int rank = kv.first;
    if (!win_storage_manager.GetStorageByNameRank(name, rank,
                                                  bf_neighbor_tensor)) {
      BFLOG(FATAL) << "Cannot get neighbor tensor with " << name << " at rank "
                   << rank;
      return 0;
    }
    bf_neighbor_tensor->GetUnderlyingTensor().fill_(0.0);
    if (associated_with_p) {
      common::SetWinAssociatedPByNameAndRank(name, rank, 0.0);
    }
  }
  return 1;
}

}  // namespace

int DoWinSync(::torch::Tensor tensor, const std::string& name,
              double self_weight,
              const std::unordered_map<int, double>& neighbor_weights,
              bool reset, bool internal_avg, bool require_mutex) {
  ThrowIfError(common::CheckInitialized());

  Timeline* timeline_ptr;
  Status timeline_status = GetBluefogTimeline(timeline_ptr);
  timeline_ptr->ActivityStart(name, "WIN_SYNC_COMPUTE_AVERAGE");

  int device = CPU_DEVICE_ID;
  if (!win_storage_manager.GetDeviceByName(name, &device)) {
    BFLOG(ERROR) << "Cannot get device of win " << name;
    return 0;
  }

  // We need to lock self avoid updating and win_put/win_accumulate happen at
  // simultaneous time.
  std::vector<int> neighbor_ranks;
  neighbor_ranks.reserve(neighbor_weights.size());
  for (auto& kv : neighbor_weights) {
    neighbor_ranks.push_back(kv.first);
  }
  if (require_mutex)
    common::WindowMutexAcquire(name, neighbor_ranks, device, /*is_sync=*/true);

  bool associated_with_p = common::GetWinOpsWithAssociatedPState();
  Status status = common::WindowSync(name, device);

  ::torch::Tensor tensor_buffer = tensor;
  if (WIN_ON_CPU && tensor.device().is_cuda()) {
    tensor_buffer =
        tensor.to(::torch::Device(::torch::kCPU), /*non_blocking=*/false);
  }

  // internal_avg specifies the detailed flow for weighted reduction operation
  // for the neighbors which may lead to efficiency and precision difference.
  // but when internal_avg is false, the results are only correct when all
  // weights are 1/(neighbor size+1).
  if (internal_avg) {
    // Weighted averaging with neighbors' tensors happens in-place.
    if (!win_storage_manager.AvgWithNeighbor(name, tensor_buffer, self_weight,
                                             neighbor_weights, associated_with_p)) {
      if (require_mutex)
        common::WindowMutexRelease(name, neighbor_ranks, device, /*is_sync=*/true);
      return 0;
    }
  } else {
    // Sum over neighbors' tensors happens in-place.
    if (!win_storage_manager.SumWithNeighbor(name, tensor_buffer, associated_with_p)) {
      if (require_mutex)
        common::WindowMutexRelease(name, neighbor_ranks, device, /*is_sync=*/true);
      return 0;
    }
    // +1 here because in neighbor degree doesn't include self rank.
    double neighbor_size = neighbor_weights.size() + 1.0;
    tensor_buffer.div_(neighbor_size);
    if (associated_with_p) {
      double associated_p = GetWinAssociatedP(name);
      SetWinAssociatedP(name, associated_p / neighbor_size);
    }
  }

  if (reset && !ResetNeighborTensor(name, neighbor_weights, associated_with_p)) {
    if (require_mutex)
      common::WindowMutexRelease(name, neighbor_ranks, device, /*is_sync=*/true);
    return 0;
  }
  if (require_mutex)
    common::WindowMutexRelease(name, neighbor_ranks, device, /*is_sync=*/true);

  if (WIN_ON_CPU && tensor.device().is_cuda()) {
    auto device = GetDeviceID(tensor);
    with_device device_guard(device);
    tensor.copy_(tensor_buffer);
    // TODO(ybc) When pull_get is used in GPU, we need to copy twice here. Optimizer it.
    win_storage_manager.SetSelfStorageByName(name, tensor);
  }
  timeline_ptr->ActivityEnd(name);  // WIN_SYNC_COMPUTE_AVERAGE

  return 1;
}

int DoWinFree(const std::string& name) {
  ThrowIfError(common::CheckInitialized());

  int device = CPU_DEVICE_ID;
  if (name.empty()) {
    win_storage_manager.ClearAll();
  } else {
    if(!win_storage_manager.GetDeviceByName(name, &device)) {
      BFLOG(ERROR) << "Cannot get device of win " << name;
      return 0;
    }
    auto res = win_storage_manager.UnregisterWinName(name);
    if (!res) {
      BFLOG(ERROR) << "Cannot unregister win " << name;
      return 0;
    }
  }

  auto handle = win_handle_manager.AllocateHandle();
  auto enqueue_result = common::EnqueueTensorWindowFree(
      name, device, [handle](const Status& status) {
        win_handle_manager.MarkDone(handle, status);
      });
  ThrowIfError(enqueue_result);
  // Blocking ops. Wait until it is done.
  DoWinWait(handle);
  return 1;
}

int DoWinPut(::torch::Tensor tensor, const std::string& name,
             const double self_weight,
             const std::unordered_map<int, double>& dst_weights,
             const bool require_mutex) {
  ThrowIfError(common::CheckInitialized());

  Timeline* timeline_ptr;
  Status timeline_status = GetBluefogTimeline(timeline_ptr);
  timeline_ptr->ActivityStart(name, "ENQUEUE_WIN_PUT");

  auto device = GetDeviceID(tensor);
  auto handle = win_handle_manager.AllocateHandle();
  // Have to get that value here since it will be used in callback, of which
  // might change will wait for communication.
  bool associated_with_p = common::GetWinOpsWithAssociatedPState();

  std::shared_ptr<TorchTensor> bf_tensor;

  if (WIN_ON_CPU && tensor.device().is_cuda()) {
    // TODO(ybc) Use non_blocking copy and ready_event to make it faster?
    ::torch::Tensor cpu_buffer =
        tensor.to(::torch::Device(::torch::kCPU), /*non_blocking=*/false);
    bf_tensor = std::make_shared<TorchTensor>(cpu_buffer);
    device = CPU_DEVICE_ID;
  } else {
    bf_tensor = std::make_shared<TorchTensor>(tensor);
  }

  // Note callback function will be called by different thread.
  std::thread::id tid = std::this_thread::get_id();
  auto enqueue_result = EnqueueTensorWindowPut(
      bf_tensor, name, dst_weights, device, require_mutex,
      [handle, name, timeline_ptr, tid, tensor, self_weight,
       associated_with_p](const Status& status) mutable {
        if (status.ok()) {
          if (self_weight != 1.0) {
            tensor.mul_(self_weight);
          }
          if (associated_with_p) {
            double old_value = GetWinAssociatedP(name);
            SetWinAssociatedP(name, old_value * self_weight);
          }
        }
        win_handle_manager.MarkDone(handle, status);
        timeline_ptr->ActivityEnd(name, &tid);  // ENQUEUE
      });

  ThrowIfError(enqueue_result);
  return handle;
}

int DoWinAccumulate(::torch::Tensor tensor, const std::string& name,
                    const double self_weight,
                    const std::unordered_map<int, double>& dst_weights,
                    const bool require_mutex) {
  ThrowIfError(common::CheckInitialized());

  Timeline* timeline_ptr;
  Status timeline_status = GetBluefogTimeline(timeline_ptr);
  timeline_ptr->ActivityStart(name, "ENQUEUE_WIN_ACCUMULATE");

  auto device = GetDeviceID(tensor);
  auto handle = win_handle_manager.AllocateHandle();
  // Have to get that value here since it will be used in callback, of which
  // might change will wait for communication.
  bool associated_with_p = common::GetWinOpsWithAssociatedPState();

  std::shared_ptr<TorchTensor> bf_tensor;

  if (WIN_ON_CPU && tensor.device().is_cuda()) {
    ::torch::Tensor cpu_buffer =
        tensor.to(::torch::Device(::torch::kCPU), /*non_blocking=*/false);
    bf_tensor = std::make_shared<TorchTensor>(cpu_buffer);
    device = CPU_DEVICE_ID;
  } else {
    bf_tensor = std::make_shared<TorchTensor>(tensor);
  }

  // Note callback function will be called by different thread.
  std::thread::id tid = std::this_thread::get_id();
  auto enqueue_result = EnqueueTensorWindowAccumulate(
      bf_tensor, name, dst_weights, device, require_mutex,
      [handle, name, timeline_ptr, tid, tensor, self_weight,
       associated_with_p](const Status& status) mutable {
        if (status.ok()) {
          if (self_weight != 1.0) {
            tensor.mul_(self_weight);
          }
          if (associated_with_p) {
            double old_value = GetWinAssociatedP(name);
            SetWinAssociatedP(name, old_value * self_weight);
          }
        }
        win_handle_manager.MarkDone(handle, status);
        timeline_ptr->ActivityEnd(name, &tid);  // ENQUEUE
      });

  ThrowIfError(enqueue_result);
  return handle;
}

int DoWinGet(const std::string& name,
             const std::unordered_map<int, double>& src_weights,
             const bool require_mutex) {
  ThrowIfError(common::CheckInitialized());

  Timeline* timeline_ptr;
  Status timeline_status = GetBluefogTimeline(timeline_ptr);
  timeline_ptr->ActivityStart(name, "ENQUEUE_WIN_GET");

  auto handle = win_handle_manager.AllocateHandle();
  int device = CPU_DEVICE_ID;
  if (!win_storage_manager.GetDeviceByName(name, &device)) {
    BFLOG(ERROR) << "Cannot get device of win " << name;
    return 0;
  }
  // Note callback function will be called by different thread.
  auto enqueue_result = EnqueueTensorWindowGet(
      name, src_weights, device, require_mutex,
      [handle, name, src_weights, timeline_ptr](const Status& status) mutable {
        std::shared_ptr<TorchTensor> bf_neighbor_tensor;
        for (auto& kv : src_weights) {
          int rank = kv.first;
          float weight = kv.second;
          if (!win_storage_manager.GetStorageByNameRank(name, rank,
                                                        bf_neighbor_tensor)) {
            BFLOG(FATAL) << "Cannot get neighbor tensor with " << name
                         << " at rank " << rank;
          }
          bf_neighbor_tensor->GetUnderlyingTensor().mul_(weight);
        }
        win_handle_manager.MarkDone(handle, status);
        timeline_ptr->ActivityEnd(name);  // ENQUEUE
      });

  ThrowIfError(enqueue_result);
  return handle;
}

int DoWinPollHandle(int handle) {
  return win_handle_manager.PollHandle(handle) ? 1 : 0;
}

void DoWinWait(int handle) {
  while (!win_handle_manager.PollHandle(handle)) {
    std::this_thread::sleep_for(std::chrono::microseconds(1));
  }
  auto status = win_handle_manager.ReleaseHandle(handle);
  ThrowIfError(*status);
}

int DoWinFence(const std::string& name) {
  ThrowIfError(common::CheckInitialized());
  Status status = common::WindowFence(name);
  return status.ok() ? 1 : 0;
}

void DoWinLock(const std::string& name) {
  ThrowIfError(common::CheckInitialized());
  Status status = common::WindowLock(name);
  ThrowIfError(status);
}

void DoWinUnlock(const std::string& name) {
  ThrowIfError(common::CheckInitialized());
  Status status = common::WindowUnlock(name);
  ThrowIfError(status);
}

void DoWinMutexAcquire(const std::string& name, const std::vector<int>& ranks,
                       bool is_sync) {
  ThrowIfError(common::CheckInitialized());
  int device = CPU_DEVICE_ID;
  if (!win_storage_manager.GetDeviceByName(name, &device)) {
    ThrowIfError(Status::InvalidArgument("Cannot get device of win " + name));
  }
  Status status =
      common::WindowMutexAcquire(name, ranks, device, /*is_sync=*/is_sync);
  ThrowIfError(status);
}

void DoWinMutexRelease(const std::string& name, const std::vector<int>& ranks,
                       bool is_sync) {
  ThrowIfError(common::CheckInitialized());
  int device = CPU_DEVICE_ID;
  if (!win_storage_manager.GetDeviceByName(name, &device)) {
    ThrowIfError(Status::InvalidArgument("Cannot get device of win " + name));
  }
  Status status =
      common::WindowMutexRelease(name, ranks, device, /*is_sync=*/is_sync);
  ThrowIfError(status);
}

std::vector<int> GetWinVersion(char* name,
                  std::vector<int>& versions) {
  ThrowIfError(common::CheckInitialized());
  Status status =
      common::GetWindowVersion(name, versions);
  ThrowIfError(status);
  return versions;
}

void SetWinOpsWithAssociatedPState(bool value) {
  common::SetWinOpsWithAssociatedPState(value);
}

void AddWinOpsIntoPybind(py::module& m) {
  // one-sided communication
  m.def("bluefog_torch_win_create_torch_IntTensor", &DoWinCreate);
  m.def("bluefog_torch_win_create_torch_LongTensor", &DoWinCreate);
  m.def("bluefog_torch_win_create_torch_FloatTensor", &DoWinCreate);
  m.def("bluefog_torch_win_create_torch_DoubleTensor", &DoWinCreate);
#if HAVE_CUDA
  m.def("bluefog_torch_win_create_torch_cuda_IntTensor", &DoWinCreate);
  m.def("bluefog_torch_win_create_torch_cuda_LongTensor", &DoWinCreate);
  m.def("bluefog_torch_win_create_torch_cuda_FloatTensor", &DoWinCreate);
  m.def("bluefog_torch_win_create_torch_cuda_DoubleTensor", &DoWinCreate);
#endif

  m.def("bluefog_torch_win_sync_torch_IntTensor", &DoWinSync);
  m.def("bluefog_torch_win_sync_torch_LongTensor", &DoWinSync);
  m.def("bluefog_torch_win_sync_torch_FloatTensor", &DoWinSync);
  m.def("bluefog_torch_win_sync_torch_DoubleTensor", &DoWinSync);
#if HAVE_CUDA
  m.def("bluefog_torch_win_sync_torch_cuda_IntTensor", &DoWinSync);
  m.def("bluefog_torch_win_sync_torch_cuda_LongTensor", &DoWinSync);
  m.def("bluefog_torch_win_sync_torch_cuda_FloatTensor", &DoWinSync);
  m.def("bluefog_torch_win_sync_torch_cuda_DoubleTensor", &DoWinSync);
#endif

  m.def("bluefog_torch_win_put_torch_IntTensor", &DoWinPut);
  m.def("bluefog_torch_win_put_torch_LongTensor", &DoWinPut);
  m.def("bluefog_torch_win_put_torch_FloatTensor", &DoWinPut);
  m.def("bluefog_torch_win_put_torch_DoubleTensor", &DoWinPut);
#if HAVE_CUDA
  m.def("bluefog_torch_win_put_torch_cuda_IntTensor", &DoWinPut);
  m.def("bluefog_torch_win_put_torch_cuda_LongTensor", &DoWinPut);
  m.def("bluefog_torch_win_put_torch_cuda_FloatTensor", &DoWinPut);
  m.def("bluefog_torch_win_put_torch_cuda_DoubleTensor", &DoWinPut);
#endif

  m.def("bluefog_torch_win_accumulate_torch_IntTensor", &DoWinAccumulate);
  m.def("bluefog_torch_win_accumulate_torch_LongTensor", &DoWinAccumulate);
  m.def("bluefog_torch_win_accumulate_torch_FloatTensor", &DoWinAccumulate);
  m.def("bluefog_torch_win_accumulate_torch_DoubleTensor", &DoWinAccumulate);
#if HAVE_CUDA
  m.def("bluefog_torch_win_accumulate_torch_cuda_IntTensor", &DoWinAccumulate);
  m.def("bluefog_torch_win_accumulate_torch_cuda_LongTensor", &DoWinAccumulate);
  m.def("bluefog_torch_win_accumulate_torch_cuda_FloatTensor",
        &DoWinAccumulate);
  m.def("bluefog_torch_win_accumulate_torch_cuda_DoubleTensor",
        &DoWinAccumulate);
#endif

  m.def("bluefog_torch_win_get", &DoWinGet);

  m.def("bluefog_torch_win_free", &DoWinFree);
  m.def("bluefog_torch_win_fence", &DoWinFence);
  m.def("bluefog_torch_win_poll", &DoWinPollHandle);
  m.def("bluefog_torch_win_wait", &DoWinWait);

  m.def("bluefog_torch_win_lock", &DoWinLock);
  m.def("bluefog_torch_win_unlock", &DoWinUnlock);

  m.def("bluefog_torch_win_mutex_acquire", &DoWinMutexAcquire);
  m.def("bluefog_torch_win_mutex_release", &DoWinMutexRelease);

  m.def("bluefog_torch_get_win_version", &GetWinVersion);
  
  m.def("bluefog_torch_win_associated_p", &GetWinAssociatedP);
  m.def("bluefog_torch_set_win_ops_with_associated_p_state", &SetWinOpsWithAssociatedPState);
}

}  // namespace torch
}  // namespace bluefog

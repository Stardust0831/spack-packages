# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.generic import Package

from spack.package import *

_versions = {
    "0.9.1.3056-cuda130": {
        "Linux-x86_64": dict(
            sha256="9de8de5f505a0a5f353c7a52259450e364418b2c645bf08da2a550731a09b8f8",
            url="https://developer.download.nvidia.com/compute/cublasmp/redist/libcublasmp/linux-x86_64/libcublasmp-linux-x86_64-0.9.1.3056_cuda13-archive.tar.xz",
        ),
        "Linux-aarch64": dict(
            sha256="eedfce3afd25db78e2fc1695b63dc460c208d79830e5574d4f5ed6dec77d553e",
            url="https://developer.download.nvidia.com/compute/cublasmp/redist/libcublasmp/linux-sbsa/libcublasmp-linux-sbsa-0.9.1.3056_cuda13-archive.tar.xz",
        ),
    },
    "0.9.1.3056-cuda120": {
        "Linux-x86_64": dict(
            sha256="35fea4df2bb08a496981f34c0d486f0753d3766a31d60dbe6daa6f16673cd1cc",
            url="https://developer.download.nvidia.com/compute/cublasmp/redist/libcublasmp/linux-x86_64/libcublasmp-linux-x86_64-0.9.1.3056_cuda12-archive.tar.xz",
        ),
        "Linux-aarch64": dict(
            sha256="51aed588b7faf5c96c283010792c7fa703311037867ef9a5f99af5f3e04e4623",
            url="https://developer.download.nvidia.com/compute/cublasmp/redist/libcublasmp/linux-sbsa/libcublasmp-linux-sbsa-0.9.1.3056_cuda12-archive.tar.xz",
        ),
    },
    "0.5.0.898": {
        "Linux-x86_64": dict(
            sha256="e8bc831d743bbbf5f5af8b728ab4da74acdcea37c4ee1022e63f8f537d5488a2",
            url="https://developer.download.nvidia.com/compute/cublasmp/redist/libcublasmp/linux-x86_64/libcublasmp-linux-x86_64-0.5.0.898_cuda12-archive.tar.xz",
        ),
        "Linux-aarch64": dict(
            sha256="6e548a11bd6ba6c4aef77c9d1c16bdc39b7ec268547f856c5dab39085fbb7fd4",
            url="https://developer.download.nvidia.com/compute/cublasmp/redist/libcublasmp/linux-sbsa/libcublasmp-linux-sbsa-0.5.0.898_cuda12-archive.tar.xz",
        ),
    },
}


class Cublasmp(Package, CudaPackage):
    """
    NVIDIA cuBLASMp is a high-performance, multi-process, GPU-accelerated library
    for distributed basic dense linear algebra.
    """

    homepage = "https://docs.nvidia.com/cuda/cublasmp/"
    url = "https://developer.download.nvidia.com/compute/cublasmp/redist/libcublasmp/"

    maintainers("albestro")

    license("UNKNOWN")

    for ver, packages in _versions.items():
        package = packages.get(f"{platform.system()}-{platform.machine()}")
        if package:
            version(ver, **package)

    conflicts("~cuda", msg="cuBLASMp requires CUDA")

    cuda120_versions = ("@0.9.1.3056-cuda120", "@0.5.0.898")
    cuda130_versions = ("@0.9.1.3056-cuda130",)
    nccl_versions = ("@0.9.1.3056-cuda120", "@0.9.1.3056-cuda130")

    for v in cuda120_versions:
        depends_on("cuda@12", when=v, type=("build", "link", "run"))
    for v in cuda130_versions:
        depends_on("cuda@13", when=v, type=("build", "link", "run"))

    depends_on("nvshmem@3.1:", when="@0.5.0.898", type=("build", "link", "run"))
    depends_on("nccl@2.18.5:", when="@0.5.0.898", type=("build", "link", "run"))
    for v in nccl_versions:
        depends_on("nccl@2.29.2:", when=v, type=("build", "link", "run"))

    for cuda_arch in CudaPackage.cuda_arch_values:
        with when(f"cuda_arch={cuda_arch}"):
            depends_on(
                f"nvshmem cuda_arch={cuda_arch}",
                when="@0.5.0.898",
                type=("build", "link", "run"),
            )
            depends_on(f"nccl cuda_arch={cuda_arch}", type=("build", "link", "run"))

    def install(self, spec, prefix):
        install_tree(".", prefix)

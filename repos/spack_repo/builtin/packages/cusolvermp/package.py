# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack_repo.builtin.build_systems.cuda import CudaPackage
from spack_repo.builtin.build_systems.generic import Package

from spack.package import *

_versions = {
    "0.9.0.6427-cuda130": {
        "Linux-x86_64": dict(
            sha256="982d8fb45912e34d5b037fef2bce3f3178ba1459bf6e1747a10d0a1b51d31a81",
            url="https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp/linux-x86_64/libcusolvermp-linux-x86_64-0.9.0.6427_cuda13-archive.tar.xz",
        ),
        "Linux-aarch64": dict(
            sha256="978fa1599fc7ad20edd67f6d9620c0dcb968df4e885966d2acc57c7858843b07",
            url="https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp/linux-sbsa/libcusolvermp-linux-sbsa-0.9.0.6427_cuda13-archive.tar.xz",
        ),
    },
    "0.9.0.6427-cuda120": {
        "Linux-x86_64": dict(
            sha256="3b071ce69c6a6a6bb7add8784e6a3fc54e9a64a8f2c1c7da40b03bcde39eb57c",
            url="https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp/linux-x86_64/libcusolvermp-linux-x86_64-0.9.0.6427_cuda12-archive.tar.xz",
        ),
        "Linux-aarch64": dict(
            sha256="f9afae16b3356fa2c87c196c20fc0fbca5e5ad200d1aacaa8f88897020d19370",
            url="https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp/linux-sbsa/libcusolvermp-linux-sbsa-0.9.0.6427_cuda12-archive.tar.xz",
        ),
    },
    "0.7.2.888": {
        "Linux-x86_64": dict(
            sha256="70243423e07861007ca5a95d35247af4ecdbcd0bf77aa09016a1abf3dcffb6a8",
            url="https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp/linux-x86_64/libcusolvermp-linux-x86_64-0.7.2.888_cuda12-archive.tar.xz",
        ),
        "Linux-aarch64": dict(
            sha256="4c1a2688ec0072dec6d9d2303b489a48ad34a419e42ba05f51af68a43221fed6",
            url="https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp/linux-sbsa/libcusolvermp-linux-sbsa-0.7.2.888_cuda12-archive.tar.xz",
        ),
    },
    "0.7.0.833": {
        "Linux-x86_64": dict(
            sha256="5383f35eefd45cc0a5cbd173a4a353941f02b912eb2f8d3a85c30345054df5e9",
            url="https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp/linux-x86_64/libcusolvermp-linux-x86_64-0.7.0.833_cuda12-archive.tar.xz",
        ),
        "Linux-aarch64": dict(
            sha256="a0012c5be7ac742a26cf8894bed3c703edea84eddf0d5dca42d35582622ffb9b",
            url="https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp/linux-sbsa/libcusolvermp-linux-sbsa-0.7.0.833_cuda12-archive.tar.xz",
        ),
    },
}


class Cusolvermp(Package, CudaPackage):
    """
    NVIDIA cuSOLVERMp is a high-performance, distributed-memory, GPU-accelerated library
    that provides tools for the solution of dense linear systems and eigenvalue problems.
    """

    homepage = "https://docs.nvidia.com/cuda/cusolvermp/"
    url = "https://developer.download.nvidia.com/compute/cusolvermp/redist/libcusolvermp"

    maintainers("albestro")

    redistribute(source=False, binary=False)

    # https://docs.nvidia.com/cuda/cusolvermp/license.html
    license("NVIDIA Software License Agreement")

    for ver, packages in _versions.items():
        package = packages.get(f"{platform.system()}-{platform.machine()}")
        if package:
            version(ver, **package)

    conflicts("~cuda", msg="cuSOLVERMp requires CUDA")

    cuda120_versions = ("@0.9.0.6427-cuda120", "@0.7.2.888", "@0.7.0.833")
    cuda130_versions = ("@0.9.0.6427-cuda130",)
    cublasmp_versions = ("@0.9.0.6427-cuda120", "@0.9.0.6427-cuda130")

    for v in cuda120_versions:
        depends_on("cuda@12", when=v, type=("build", "link", "run"))
    for v in cuda130_versions:
        depends_on("cuda@13", when=v, type=("build", "link", "run"))

    depends_on("nccl@2.18.5:", type=("build", "link", "run"))
    for v in cublasmp_versions:
        depends_on("cublasmp@0.9.1: +cuda", when=v, type=("build", "link", "run"))

    for cuda_arch in CudaPackage.cuda_arch_values:
        with when(f"cuda_arch={cuda_arch}"):
            depends_on(f"nccl cuda_arch={cuda_arch}", type=("build", "link", "run"))
            for v in cublasmp_versions:
                depends_on(
                    f"cublasmp cuda_arch={cuda_arch}",
                    when=v,
                    type=("build", "link", "run"),
                )

    def install(self, spec, prefix):
        install_tree(".", prefix)

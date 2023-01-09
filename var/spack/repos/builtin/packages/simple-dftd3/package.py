# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SimpleDftd3(MesonPackage):
    """
    Simple reimplementation of the DFT-D3 dispersion correction
    """

    homepage = "https://dftd3.readthedocs.io"
    url = "https://github.com/dftd3/simple-dftd3/releases/download/v0.6.0/s-dftd3-0.6.0-source.tar.xz"
    git = "https://github.com/dftd3/simple-dftd3.git"

    maintainers = ["awvwgk"]

    version("main", branch="main")
    version("0.6.0", "c057361565f570cb128489c70131487f71b6891a40e5292dfe37041596810dfe")
    version("0.5.1", "0411fdaebe438f652a970cb232ae3199c4cc840366ed05fda4c38e634632040d")

    variant("openmp", default=True, description="Use OpenMP parallelisation")
    variant("python", default=False, description="Build Python extension module")

    depends_on("mctc-lib")
    depends_on("meson@0.57.1:", type="build")  # mesonbuild/meson#8377
    depends_on("pkgconfig", type="build")
    depends_on("toml-f")
    depends_on("py-cffi", when="+python")
    depends_on("python@3.6:", when="+python")

    def meson_args(self):

        return [
            "-Dopenmp={0}".format(str("+openmp" in self.spec).lower()),
            "-Dpython={0}".format(str("+python" in self.spec).lower()),
        ]

    def setup_run_environment(self, env):
        if "+python" in self.spec:
            pydir = join_path(
                self.prefix.lib,
                "python" + str(self.spec["python"].version.up_to(2)),
                "site-packages",
            )
            env.prepend_path("PYTHONPATH", pydir)

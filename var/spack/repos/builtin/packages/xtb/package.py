# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install xtb
#
# You can edit this file again by typing:
#
#     spack edit xtb
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Xtb(CMakePackage):
    """
    Semiempirical Extended Tight-Binding Program Package
    """

    homepage = "https://xtb-docs.readthedocs.io"
    url = "https://github.com/grimme-lab/xtb/releases/download/v6.5.0/xtb-6.5.0-source.tar.xz"

    maintainers = ["awvwgk"]

    version("6.5.0", "5f780656bf7b440a8e1f753a9a877401a7d497fb3160762f48bdefc8a9914976")

    depends_on("blas")
    depends_on("cmake", type="build")
    depends_on("lapack")
    depends_on("meson@0.57.1:", type="build")  # mesonbuild/meson#8377
    depends_on("pkgconfig", type="build")

    def meson_args(self):

        return [
            "-Dla_backend=custom",
            "-Dcustom_libraries={0}".format(','.join(self.spec["lapack"].libs.names)),
            "-Dopenmp={0}".format(str("+openmp" in self.spec).lower()),
        ]

# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Minizip(AutotoolsPackage):
    """C library for zip/unzip via zLib."""

    homepage = "https://www.winimage.com/zLibDll/minizip.html"
    url = "https://zlib.net/fossils/zlib-1.2.11.tar.gz"

    license("Zlib")

    version("1.3.1", sha256="9a93b2b7dfdac77ceba5a558a580e74667dd6fede4585b91eefb60f03b72df23")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2022-37434
        version(
            "1.2.11", sha256="c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1"
        )

    depends_on("c", type="build")

    configure_directory = "contrib/minizip"

    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("zlib-api")

    # error: implicit declaration of function 'mkdir' is invalid in C99
    with when("@:1.2.11"):
        patch("implicit.patch", when="%apple-clang@12:")
        patch("implicit.patch", when="%gcc@7.3.0:")

    # statically link to libz.a
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/minizip.rb
    patch("static.patch", when="%apple-clang@12:")

    # build minizip and miniunz
    @run_before("autoreconf")
    def build_minizip_binary(self):
        configure()
        make()
        with working_dir(self.configure_directory):
            make()

    # install minizip and miniunz
    @run_after("install")
    def install_minizip_binary(self):
        mkdirp(self.prefix.bin)
        with working_dir(self.configure_directory):
            install("minizip", self.prefix.bin)
            install("miniunz", self.prefix.bin)

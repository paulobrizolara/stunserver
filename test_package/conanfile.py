#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment

import os
from os import path

package_name = "stuntman"
version      = "1.2.13"
username     = os.getenv("CONAN_USERNAME", "notfound")
channel      = os.getenv("CONAN_CHANNEL", "testing")

class TestConanFile(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    #Conan dependencies
    requires = (
        "%s/%s@%s/%s" % (package_name, version, username, channel),

        "waf/0.1.1@paulobrizolara/stable",
        "WafGenerator/0.0.4@paulobrizolara/testing"
    )

    generators = "Waf"
    exports = "wscript"

    def imports(self):
        # Copy waf executable to project folder
        self.copy("waf", dst=".")

        self.copy("*.dll", dst="bin", src="bin")    # From bin to bin
        self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

    def build(self):
        self.build_path = path.abspath("build")

        self.output.info("conanfile_dir: " + self.conanfile_directory)
        self.run(
            "waf configure build -o %s" % (self.build_path),
            cwd=self.conanfile_directory)

    def test(self):
        exec_path = path.join(self.build_path, 'example')
        self.output.info("running test: " + exec_path)
        self.run(exec_path)

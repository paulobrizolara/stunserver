#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment

import os
from os import path

class Recipe(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    #Conan dependencies
    requires = (
        "OpenSSL/1.0.2k@lasote/stable",
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

        self.run(
            "waf configure build -o %s" % (self.build_path),
            cwd=self.conanfile_directory)

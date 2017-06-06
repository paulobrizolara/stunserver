#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, AutoToolsBuildEnvironment

import os
from os import path

class Recipe(ConanFile):
    name        = "stuntman"
    version     = "1.2.13.1"
    description = "STUN server and client code by john selbie"
    license     = "Apache 2.0"
    url         = "https://github.com/jselbie/stunserver"

    settings = "os", "compiler", "build_type", "arch"

    #Conan dependencies
    requires = (
        "OpenSSL/1.0.2k@lasote/stable",
        "Boost/1.62.0@lasote/stable",

        "waf/0.1.1@paulobrizolara/stable",
        "WafGenerator/0.0.4@paulobrizolara/testing"
    )

    generators = "Waf"
    exports_sources = (
        "wscript",
        "client/**",
        "common/**",
        "networkutils/**",
        "server/**",
        "stuncore/**",
        "resources/**",
        "testcode/**"
    )
    options = {
        "shared"            : [True, False]
    }
    default_options     = (
        'shared=False',
        'Boost:header_only=True'
    )

    def imports(self):
        # Copy waf executable to project folder
        self.copy("waf", dst=".")

        self.copy("*.dll", dst="bin", src="bin")    # From bin to bin
        self.copy("*.dylib*", dst="bin", src="lib") # From lib to bin

    def build(self):
        self.build_path = path.abspath("build")

        self.run(
            "waf configure build install -o %s %s" % (self.build_path, self.get_options()),
            cwd=self.conanfile_directory)


    def package_info(self):
        self.cpp_info.libs    = ['stuntman']
        self.cpp_info.bindirs = ["bin"]

    def get_options(self):
        opts = []

        if self.settings.build_type == "Debug":
            opts.append("--debug")
        else:
            opts.append("--release")

        if self.options.shared:
            self.output.info("building shared library")
            opts.append("--shared")

        if not hasattr(self, "package_folder"):
            self.package_folder = path.abspath(path.join(".", "package"))

        opts.append("--prefix=%s" % self.package_folder)

        return " ".join(opts)

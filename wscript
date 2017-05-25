#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from waflib.Configure import conf

def load_tools(ctx):
    ctx.load('compiler_cxx')
    ctx.load('gnu_dirs')

def options(ctx):
    load_tools(ctx)

    ctx.add_option('--debug', action='store_true', default=False, dest='debug', help='Do debug build')
    ctx.add_option('--release', action='store_false', dest='debug', help='Do release build')
    ctx.add_option('--profile', action='store_true', default=False, dest='profile', help='Do profile build')

    ctx.add_option('--shared', action='store_true', default=False, help='Build libs as shared libraries')

def init(ctx):
    from waflib.Options import options

    # Create build variants (i.e. independent build files)
    setup_variant(get_variant_name(options))

def configure(ctx):
    load_tools(ctx)

    ctx.load('conanbuildinfo_waf', tooldir=[".", path.join(ctx.bldnode.abspath(), "..")]);

    # global flags
    ctx.env.CXXFLAGS = get_cxx_flags(ctx)
    ctx.env.DEFINES = get_defines(ctx)

    ctx.env.shared = ctx.options.shared

def build(bld):
    for d in ('common', 'stuncore', 'networkutils', 'testcode', 'client', 'server'):
        bld.recurse(d)

######################################################################################

def get_variant_name(options):
    build_type = "debug" if options.debug else "release"

    if options.profile:
        build_type = "profile"

    lib_type = "shared" if options.shared else "static"

    return build_type + "_" + lib_type

def get_cxx_flags(ctx):
    cxxflags = ['-Wall', '-Wuninitialized']

    if not ctx.options.debug or ctx.options.profile:
        cxxflags.extend(["-O2"])

    if ctx.options.debug or ctx.options.profile:
        cxxflags.extend(["-g"])

    if ctx.options.shared:
        cxxflags.append("-fPIC")

    return cxxflags

def get_defines(ctx):
    defines = []

    if ctx.options.debug:
        defines.append("DEBUG")
    else:
        defines.append("NDEBUG")

    return defines

###################################################################################################

def setup_variant(variant_name):
    from waflib.Options import options
    from waflib.Build import BuildContext, CleanContext, InstallContext, UninstallContext
    from waflib.Configure import ConfigurationContext
    for y in (BuildContext, CleanContext, InstallContext, UninstallContext, ConfigurationContext):
        name = y.__name__.replace('Context','').lower()
        class tmp(y):
            cmd = name
            variant = variant_name

@conf
def lib(bld, *k, **kw):
    from waflib import Utils

    if 'install_path' not in kw:
        kw['install_path'] = bld.env.LIBDIR

    if bld.env.shared:
        bld.shlib(*k, **kw)
    else:
        bld.stlib(*k, **kw)

    includedir = kw.get('install_includedir', bld.env.INCLUDEDIR)

    install_headers = []

    if 'install_headers' in kw:
        install_headers = kw['install_headers']
    elif 'export_includes' in kw:

        for inc_dir in kw.get('export_includes'):

            inc_node = bld.path.make_node(inc_dir)
            incs = inc_node.ant_glob([
                                path.join('**', '*.h'),
                                path.join('**', '*.hpp')])

            install_headers.extend(incs)

    if install_headers:
        headers_base = kw.get("headers_base", None)
        relative_trick = kw.get("install_relative", True)
        bld.install_files(includedir, Utils.to_list(install_headers), relative_trick=relative_trick, cwd=headers_base)

@conf
def get_env(ctx, opt, default=None):
    if opt in ctx.env:
        return ctx.env[opt]
    else:
        return default

@conf
def glob(bld, *k, **kw):
    '''Helper to execute an ant_glob search.
        See documentation at: https://waf.io/apidocs/Node.html?#waflib.Node.Node.ant_glob
    '''

    return bld.path.ant_glob(*k, **kw)

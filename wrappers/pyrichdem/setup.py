import glob
from pybind11.setup_helpers import Pybind11Extension
from setuptools import setup
from setuptools.command.build_ext import build_ext as _build_ext

# Compiler-specific arguments
BUILD_ARGS = {
    "msvc": ["/std:c++17", "/O2"],
    "unix": ["-std=c++17", "-O3", "-fvisibility=hidden"],
}

class build_ext(_build_ext):
    def build_extensions(self):
        compiler = self.compiler.compiler_type
        args = BUILD_ARGS.get(compiler, [])
        for ext in self.extensions:
            ext.extra_compile_args = args
        _build_ext.build_extensions(self)

ext_modules = [
    Pybind11Extension(
        "_richdem",
        ["src/pywrapper.cpp"] + list(glob.glob("lib/richdem/src/**/*.cpp", recursive=True)),
        include_dirs=["lib/richdem/include"],
        define_macros=[
            ("DOCTEST_CONFIG_DISABLE", None),
            ("_USE_MATH_DEFINES", None),  # Ensure M_PI is available in MSVC
        ],
        language="c++",
    ),
]

setup(
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
)
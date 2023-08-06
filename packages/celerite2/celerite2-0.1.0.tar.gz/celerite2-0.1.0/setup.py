#!/usr/bin/env python

# Inspired by:
# https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/
import codecs
import os
import re
import sys

from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext

# PROJECT SPECIFIC

NAME = "celerite2"
PACKAGES = find_packages(where="python")
META_PATH = os.path.join("python", "celerite2", "__init__.py")
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
]
INSTALL_REQUIRES = ["numpy>=1.13.0"]
SETUP_REQUIRES = INSTALL_REQUIRES + [
    "pybind11>=2.4",
    "setuptools>=40.6.0",
    "setuptools_scm",
    "wheel",
]
EXTRA_REQUIRE = {
    "style": ["isort", "black", "black_nbconvert"],
    "test": [
        "coverage[toml]",
        "pytest==6.0.0rc1",
        "pytest-cov",
        "scipy",
        "celerite>=0.3.1",
    ],
    "theano": ["theano"],
    "torch": ["torch"],
    "jax": ["jax", "jaxlib"],
    "release": ["pep517", "twine"],
    "docs": [
        "sphinx",
        "sphinx-material",
        "sphinx_copybutton",
        "rtds_action",
        "nbsphinx",
        "breathe",
        "ipython",
    ],
    "tutorials": [
        "jupytext",
        "jupyter",
        "nbconvert",
        "matplotlib",
        "scipy",
        "emcee",
        "pymc3",
        "tqdm",
        "numpyro",
    ],
}
EXTRA_REQUIRE["dev"] = (
    EXTRA_REQUIRE["style"]
    + EXTRA_REQUIRE["test"]
    + EXTRA_REQUIRE["release"]
    + ["pre-commit", "nbstripout", "flake8"]
)


# END PROJECT SPECIFIC

# PYBIND11


class get_pybind_include:
    def __init__(self, user=False):
        self.user = user

    def __str__(self):
        import pybind11

        return pybind11.get_include(self.user)


class get_numpy_include:
    def __str__(self):
        import numpy

        return numpy.get_include()


class custom_build_ext(build_ext):
    c_opts = {
        "msvc": ["/EHsc"],
        "unix": [],
    }
    l_opts = {
        "msvc": [],
        "unix": [],
    }

    if sys.platform == "darwin":
        darwin_opts = [
            "-stdlib=libc++",
            "-mmacosx-version-min=10.14",
            "-march=native",
        ]
        c_opts["unix"] += darwin_opts
        l_opts["unix"] += darwin_opts

    def has_flag(self, flagname):
        import tempfile

        import setuptools

        with tempfile.NamedTemporaryFile("w", suffix=".cpp") as f:
            f.write("int main (int argc, char **argv) { return 0; }")
            try:
                self.compiler.compile([f.name], extra_postargs=[flagname])
            except setuptools.distutils.errors.CompileError:
                return False
        return True

    def cpp_flag(self):
        flags = ["-std=c++17", "-std=c++14", "-std=c++11"]

        for flag in flags:
            if self.has_flag(flag):
                return flag

        raise RuntimeError(
            "Unsupported compiler. At least C++11 support is needed."
        )

    def build_extensions(self):
        ct = self.compiler.compiler_type
        opts = self.c_opts.get(ct, [])
        link_opts = self.l_opts.get(ct, [])
        if ct == "unix":
            opts.append(
                '-DVERSION_INFO="%s"' % self.distribution.get_version()
            )
            opts.append(self.cpp_flag())
            if self.has_flag("-fvisibility=hidden"):
                opts.append("-fvisibility=hidden")
        elif ct == "msvc":
            opts.append(
                '/DVERSION_INFO=\\"%s\\"' % self.distribution.get_version()
            )
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)


include_dirs = [
    "c++/include",
    "c++/vendor/eigen",
    "python/celerite2",
    get_numpy_include(),
    get_pybind_include(),
    get_pybind_include(user=True),
]
if "READTHEDOCS" in os.environ:
    ext_modules = []
else:
    ext_modules = [
        Extension(
            "celerite2.driver",
            ["python/celerite2/driver.cpp"],
            include_dirs=include_dirs,
            language="c++",
        ),
        Extension(
            "celerite2.backprop",
            ["python/celerite2/backprop.cpp"],
            include_dirs=include_dirs,
            language="c++",
        ),
        Extension(
            "celerite2.jax.xla_ops",
            ["python/celerite2/jax/xla_ops.cpp"],
            include_dirs=include_dirs,
            language="c++",
        ),
    ]

# END PYBIND11


HERE = os.path.dirname(os.path.realpath(__file__))


def read(*parts):
    with codecs.open(os.path.join(HERE, *parts), "rb", "utf-8") as f:
        return f.read()


def find_meta(meta, meta_file=read(META_PATH)):
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta), meta_file, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{meta}__ string.".format(meta=meta))


if __name__ == "__main__":
    setup(
        name=NAME,
        use_scm_version={
            "write_to": os.path.join(
                "python", NAME, "{0}_version.py".format(NAME)
            ),
            "write_to_template": '__version__ = "{version}"\n',
        },
        author=find_meta("author"),
        author_email=find_meta("email"),
        maintainer=find_meta("author"),
        maintainer_email=find_meta("email"),
        url=find_meta("uri"),
        license=find_meta("license"),
        description=find_meta("description"),
        long_description=read("README.md"),
        long_description_content_type="text/markdown",
        packages=PACKAGES,
        package_dir={"": "python"},
        include_package_data=True,
        install_requires=INSTALL_REQUIRES,
        setup_requires=SETUP_REQUIRES,
        extras_require=EXTRA_REQUIRE,
        classifiers=CLASSIFIERS,
        zip_safe=False,
        ext_modules=ext_modules,
        cmdclass={"build_ext": custom_build_ext},
    )

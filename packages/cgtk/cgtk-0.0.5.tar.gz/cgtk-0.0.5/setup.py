from setuptools import setup
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# This call to setup() does all the work
setup(
    name="cgtk",
    version="0.0.5",
    description="generate code with python in source file comment",
    url="https://github.com/xchern/cgtk",
    author="Xiaosong Chen",
    author_email="xiaosong0911@gmail.com",
    license="MIT",
    packages=["cgtk"],
    include_package_data=False,
)
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext
from setuptools.extension import Extension
import subprocess

class CustomBuildExtCommand(build_ext):
    def run(self):
        # Run custom build commands for C code
        subprocess.check_call(['make'])  # Assuming you have a Makefile to build C code
        super().run()

setup(
    name="dcov",
    version="0.1.0",
    author="Senyi Li",
    author_email="lisy@std.uestc.edu.cn",
    description="A description of your project",
    long_description=open("README.MD").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    cmdclass={
        'build_ext': CustomBuildExtCommand,
    },
    data_files=[
        ('lib', [
            'dcov/libdcov_info.so',
            'dcov/libdcov_trace.so',
            'dcov/libdcov_ins.so',
            'dcov/probe.so'
        ]),
        ('bin', ['dcov/dcov_ins_server']),  # Copy the binary executable to the bin directory
    ],
)


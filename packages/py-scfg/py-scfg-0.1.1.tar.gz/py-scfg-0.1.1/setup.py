import os

from setuptools import find_packages, setup

if os.path.exists("README.rst"):
    long_description = open("README.rst", "r").read()
else:
    long_description = (
        "See https://hg.code.netlandish.com/~petersanchez/py-scfg"
    )


setup(
    name="py-scfg",
    version="0.1.1",
    packages=find_packages(),
    description="Module to read scfg formatted configuration files.",
    author="Peter Sanchez",
    author_email="pjs@petersanchez.com",
    url="https://hg.code.netlandish.com/~petersanchez/py-scfg",
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
)

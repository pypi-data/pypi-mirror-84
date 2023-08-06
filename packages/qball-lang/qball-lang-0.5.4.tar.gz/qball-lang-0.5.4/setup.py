import runpy
from setuptools import setup, find_packages
import os

# Requirements.txt errors


PACKAGE_NAME = "qball-lang"
VERSION = "0.5.4"

with open("README.md", "r") as fh:
    long_description = fh.read()


def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    if os.path.exists(filename):
        temp = open(filename)
        lineiter = (line.strip() for line in temp)
    else:
        open(filename, "w").write("pynput\narcade")
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version=VERSION,
        packages=find_packages(),
        install_requires=parse_requirements("requirements.txt"),
        python_requires=">=3.6.3",
        description="QBall is a high level interpreted language. This is a Python module for using QBall in python programs. Source: https://github.com/KingsleyDockerill/QBall",
        long_description=long_description,
        long_description_content_type="text/markdown",
    )

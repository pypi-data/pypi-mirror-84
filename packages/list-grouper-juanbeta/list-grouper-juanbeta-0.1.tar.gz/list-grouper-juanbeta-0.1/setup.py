
from setuptools import setup

setup(
    name='list-grouper',    # This is the name of your PyPI-package.
    version='0.1',                          # Update the version number for new releases
    scripts=['']                  # The name of your scipt, and also the command you'll be using for calling it
)

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="list-grouper-juanbeta", # Replace with your own username
    version="0.1",
    author="Juan Betancur",
    author_email="juanbeta02@gmail.com",
    description="Generates a list with enumerated groups taking into account a change in consecutive values.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
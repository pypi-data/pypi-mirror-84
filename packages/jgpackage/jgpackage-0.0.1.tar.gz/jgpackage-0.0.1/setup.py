from setuptools import find_packages, setup
from samplePackage import __version__, __author__

long_description = open("README.md").read()

setup(
    name="jgpackage",
    version=__version__,
    author=__author__,
    author_email="e@mail.com",
    maintainer="juguama",
    maintainer_email="e@mail.com",
    description="A beautiful sample package.",
    keywords=["bh", "pyladies", "tutorial"],
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.7'
)

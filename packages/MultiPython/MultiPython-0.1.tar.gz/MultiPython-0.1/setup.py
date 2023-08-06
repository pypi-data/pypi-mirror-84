from setuptools import setup
from setuptools import find_packages

classifier = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: No Input/Output (Daemon)",
    "Intended Audience :: Developers",
    "License :: Freely Distributable",
    "Natural Language :: English",
    "Operating System :: POSIX",
    "Programming Language :: Python :: 3.9",
    "Topic :: Software Development :: Interpreters"
]

setup(
    name="MultiPython",
    version="v0.1",
    description="MultiPy library for Python.",
    long_description=open("README").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mad-cs/multipy",
    authors="maDeveloper",
    author_email="",
    license="PSL",
    classifier=classifier,
    keywords="file",
    packages=find_packages(),
    install_requires=[""]
)
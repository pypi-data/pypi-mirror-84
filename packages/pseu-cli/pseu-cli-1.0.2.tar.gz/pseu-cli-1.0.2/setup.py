from setuptools import setup
from setuptools import find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="pseu-cli",
    description="A CLI tool for RNG, shuffling and other pseudorandom stuff.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.2",
    url="https://github.com/Kevinpgalligan/pseu",
    author="Kevin Galligan",
    author_email="galligankevinp@gmail.com",
    scripts=["scripts/pseu"],
    packages=find_packages("src"),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=[]
)

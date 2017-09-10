from setuptools import setup
from sys import version_info

requirements = ["beautifulsoup4", "requests"]
if sys.version_info < (2,7,3) and sys.version_info < (3,2,2):
    requirements.append("lxml")

setup(
    name = "loveroms",
    packages = ["loveroms"],
    install_requires = requirements,
    entry_points = {
        "console_scripts": ['loveroms = loveroms.loveroms:main']
        },
    version = "1.0.0",
    description = "A program to download files from loveroms",
    author = "Steven Smith",
    author_email = "stevensmith.ome@gmail.com",
    license = "MIT",
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators"
        ],
    )

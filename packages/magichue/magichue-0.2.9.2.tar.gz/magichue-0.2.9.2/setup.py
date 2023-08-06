from setuptools import setup, find_packages

import magichue

with open("README.md") as fp:
    long_description = fp.read()

setup(
    name="magichue",
    version=magichue.__version__,
    author=magichue.__author__,
    author_email="caidanstevenwilliams@gmail.com",
    description="A library to interface with MagicHue aka MagicHome.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mildmelon/python-magichue",
    license=magichue.__license__,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
        "Topic :: Utilities",
    ],
)

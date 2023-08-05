import json
from os import path

from setuptools import find_packages, setup

import boilee

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.rst"), encoding="utf-8") as file:
    long_description = file.read()

with open(path.join(here, ".gitignore"), encoding="utf-8") as file:
    ignore = [
        line.split("#")[0].rstrip()
        for line in file.readlines()
        if line.split("#")[0].rstrip()
    ]

with open(path.join(here, "Pipfile.lock"), encoding="utf-8") as lockfile:
    lockfile_dict = json.loads(lockfile.read())
    lock = {}
    lock["dependencies"] = [
        f"""{key}{value["version"]}{f"; {value['markers']}" if "markers" in value else ""}"""
        for key, value in lockfile_dict["default"].items()
    ]
    lock["dev_dependencies"] = [
        f"""{key}{value["version"]}{f"; {value['markers']}" if "markers" in value else ""}"""
        for key, value in lockfile_dict["develop"].items()
    ]

setup(
    name=boilee.__title__,
    version=boilee.__version__,
    description=boilee.__summary__,
    long_description=long_description,
    url=f"https://github.com/vadolasi/boilee",
    author=boilee.__author__,
    author_email=boilee.__email__,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="boilerplate cli generator templating",
    packages=find_packages(exclude=ignore),
    python_requires=">=3.8, <3.9",
    install_requires=lock["dependencies"],
    extras_require=dict(dev=lock["dev_dependencies"]),
    project_urls={
        "Bug Reports": f"https://github.com/vadolasi/boilee/issues",
        "Funding": "https://donate.pypi.org",
        "Say Thanks!": f"https://saythanks.io/to/vitor036daniel@gmail.com",
        "Source": f"https://github.com/vadolasi/boilee/",
    },
    entry_points=dict(
        console_scripts=["boilee=boilee.scripts.boilee:cli"],
    ),
)

#!/usr/bin/env python
"""
Package build script
"""

import os
import sys

import pip
import setuptools

LINKS = []


def get_requirements(requirements_filename, update_links=False):
    require_list = []
    try:
        # new versions of pip requires a session
        requirements = pip.req.parse_requirements(
            requirements_filename, session=pip.download.PipSession()
        )
    except:  # noqa: E722
        requirements = pip.req.parse_requirements(requirements_filename)

    for item in requirements:
        # we want to handle package names and also repo urls
        if update_links:
            if getattr(item, "url", None):  # older pip has url
                LINKS.append(str(item.url))
            if getattr(item, "link", None):  # newer pip has link
                LINKS.append(str(item.link))
        if item.req:
            require_list.append(str(item.req))
    return require_list


with open("requirements.txt") as f:
    requirements = f.read().splitlines()

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
if CURRENT_DIRECTORY in sys.path:
    sys.path.remove(CURRENT_DIRECTORY)
sys.path.insert(0, os.path.join(CURRENT_DIRECTORY, "unseal_vault"))

setuptools.setup(
    include_package_data=True,
    name="vault_unseal",
    version="0.0.1",
    install_requires=requirements,
    dependency_links=LINKS,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    # package_data={'': ['requirements.txt']},
    description="HashiCorp Vault unseal helper",
    # long_description=open("README.rst").read(),
    author="Nicolas Ledez",
    author_email="pypi.python.org@ledez.net",
    url="https://github.com/nledez/vault_python_unseal",
    keywords=["hashicorp", "vault"],
    # scripts=['manage.py'],
    packages=setuptools.find_packages(exclude=["tests"]),
    # scripts = ['unseal.py'],
    # entry_points={
    #     'console_scripts': [
    #         'unseal_vault = unseal_vault.unseal:main',
    #     ],
    # },
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Environment :: Console",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Programming Language :: Python",
    ],
)

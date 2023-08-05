#!/usr/bin/env python
from setuptools import setup

VERSION = "1.8.0"
install_reqs = ["cached-property",
                "python-dateutil",
                "six >= 1.13.0"]

test_requirements = ["pytest-cov",
                     "python-coveralls", ]

readme = open("README.rst").read()

setup(
        name="haralyzer_3",
        version=VERSION,
        description="A Python 3 for of haralyzer which is a framework for getting useful stuff out of HAR files",
        long_description=readme,
        author="Cyb3r Jak3",
        author_email="jake@jwhite.network",
        url="https://github.com/Cyb3r-Jak3/haralyzer_3",
        project_urls={
          "Changelog": "https://github.com/Cyb3r-Jak3/haralyzer_3/blob/master/HISTORY.rst",
          "Docs": "https://haralyzer-3.readthedocs.io/en/latest/"
        },
        download_url="https://github.com/mrname/haralyzer/tarball/{}".format(VERSION),
        packages=[
            "haralyzer_3"
        ],
        package_dir={"haralyzer_3": "haralyzer_3"},
        tests_require=test_requirements,
        install_requires=install_reqs,
        license="MIT",
        zip_safe=False,
        keywords="har",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: Implementation :: CPython"
        ],
)

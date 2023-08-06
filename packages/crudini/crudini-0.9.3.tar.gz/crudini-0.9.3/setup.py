# -*- coding: utf-8 -*-

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="crudini",
    version="0.9.3",
    author="Pádraig Brady",
    author_email="P@draigBrady.com",
    description=("A utility for manipulating ini files"),
    license="GPLv2",
    keywords="ini config edit",
    url="http://github.com/pixelb/crudini",
    long_description="```\n" + read('README') + "```\n",
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
    install_requires=['iniparse>=0.3.2'],
    scripts=["crudini"]
)

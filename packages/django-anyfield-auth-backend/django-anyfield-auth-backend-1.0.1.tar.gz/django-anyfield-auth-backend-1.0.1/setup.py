#!/usr/bin/env python

import os
from setuptools import setup


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="django-anyfield-auth-backend",
    version="1.0.1",
    author="Rodrigo Ristow",
    author_email="rodrigo@maxttor.com",
    description="Django Authentication backend that can use any field in the user table for identification.",
    license="BSD",
    keywords="django authentication",
    url="https://gitlab.com/rristow/django_anyfield_auth_backend",
    packages=['anyfield_auth_backend',],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


from selfauth import __version__ as VERSION

readme = open("README.md").read()

setup(
    name="selfauth",
    version=VERSION,
    description="""Self Street integration with Django for SSO.""",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Felipe Faria",
    author_email="felipe@self.st",
    url="https://github.com/column-street/django-self-auth",
    packages=["selfauth"],
    include_package_data=True,
    install_requires=[
        "Django>=3.0.0",
        "mozilla-django-oidc>=1.2.4",
        "phonenumbers>=8.12.9",
    ],
    license="BSD 3-Clause License",
    zip_safe=False,
    keywords="django-self-auth",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)

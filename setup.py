#!/usr/bin/env python

from os import path

from setuptools import setup

from longclaw import __version__

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="longclaw",
    version=__version__,
    description="""A shop for wagtail cms""",
    long_description=long_description,
    author="James Ramm",
    author_email="jamessramm@gmail.com",
    url="https://github.com/JamesRamm/longclaw",
    packages=[
        "longclaw",
    ],
    include_package_data=True,
    install_requires=[
        # "django>=2.2<3.0",
        "wagtail>=2.8",
        # "django-countries==5.5",
        "django-extensions",
        "django-ipware",
        "django-polymorphic",
    ],
    extras_require={
        "testing": [
            "mock",
            "wagtail-factories",
            "factory-boy",
        ]
    },
    license="MIT",
    zip_safe=False,
    keywords="longclaw",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)

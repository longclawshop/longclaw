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
        "wagtail>=2.15",
        "django-countries",
        "django-extensions",
        "django-ipware",
        "django-polymorphic",
    ],
    extras_require={
        "testing": [
            "mock",
            "wagtail-factories",
            "factory-boy",
            "coverage",
        ],
        "dev": [
            "black==22.10.0",
            "flake8==5.0.4",
            "isort==5.10.1",
            "pre-commit",
        ],
    },
    license="MIT",
    zip_safe=False,
    keywords="longclaw",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Django",
        "Framework :: Django :: 3",
        "Framework :: Django :: 4",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Framework :: Wagtail :: 3",
        "Framework :: Wagtail :: 4",
    ],
)

#!/usr/bin/env python
import codecs
import os

from setuptools import find_packages, setup

base_dir = os.path.dirname(__file__)

with codecs.open(os.path.join(base_dir, "README.md"), "r", encoding="utf8") as f:
    long_description = f.read()

requirements = (
    ["django>=1.11", "celery>=4.0", "django-appconf", "dnspython", "eventlet"],
)

setup(
    name="django-async-email",
    version="0.1.0",
    description="An async Django email backend using celery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="Mozilla Public License 2.0",
    url="https://github.com/eltonplima/django-async-email",
    author="Elton Lima",
    author_email="me@eltonplima.dev",
    platforms=["any"],
    packages=find_packages(exclude=["ez_setup", "tests"]),
    scripts=[],
    zip_safe=False,
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest",
            "pytest-pep8",
            "pytest-cov",
            "pytest-mock",
            "pytest-django",
            "flake8",
            "black",
            "isort",
            "tox",
            "tox-asdf",
            "freezegun",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Topic :: Communications",
        "Topic :: Communications :: Email",
        "Topic :: System :: Distributed Computing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)

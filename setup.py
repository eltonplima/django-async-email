#!/usr/bin/env python
from __future__ import absolute_import

from glob import glob
from os.path import basename
from os.path import splitext
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

BASE_DIR = Path(__file__).parent


def read(filename):
    return (BASE_DIR / filename).read_text()


requirements = (
    [
        "django>=1.11",
        "celery>=4.2.2,<5.0",
        "kombu<5.0",
        "django-appconf",
        "dnspython<2.0.0,>=1.15.0",
        "eventlet",
    ],
)

setup(
    name="django-async-email",
    version="0.1.1",
    license="Mozilla Public License 2.0",
    description="An async Django email backend using celery",
    long_description_content_type="text/markdown",
    long_description=read("README.md"),
    author="Elton Lima",
    author_email="me@eltonplima.dev",
    url="https://github.com/eltonplima/django-async-email",
    packages=find_packages("src"),
    platforms=["any"],
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 1 - Planning",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
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
    project_urls={
        "Changelog": "https://github.com/ionelmc/python-nameless/blob/master/CHANGELOG.rst",
        "Issue Tracker": "https://github.com/ionelmc/python-nameless/issues",
    },
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest",
            "pytest-pep8",
            "pytest-cov",
            "pytest-mock",
            "pytest-django",
            "pytest-celery",
            "pytest-xdist[psutil]",
            "flake8",
            "black",
            "isort",
            "tox",
            "tox-asdf",
            "freezegun",
            "wheel",
        ]
    },
    setup_requires=["pytest-runner"],
)

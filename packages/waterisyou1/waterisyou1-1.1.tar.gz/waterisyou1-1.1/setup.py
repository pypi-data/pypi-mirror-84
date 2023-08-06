# -*- coding: utf-8 -*-

# See http://pythonhosted.org/an_example_pypi_project/setuptools.html
# See https://packaging.python.org/tutorials/packaging-projects/#uploading-your-project-to-pypi

from setuptools import setup

setup(
    name='waterisyou1',
    version='1.1',
    author='Celia Oakley',
    description='A Python wrapper for The Movie Database API v3',
    keywords=['movie', 'the movie database', 'movie database', 'tmdb',
                'wrapper', 'database', 'themoviedb', 'moviedb', 'api'],
    packages=['waterisyou1'],
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
)

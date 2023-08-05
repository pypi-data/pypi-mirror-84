#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name="loo.py",
      version="2020.2",
      description="A code generator for array-based code on CPUs and GPUs",
      long_description=open("README.rst").read(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "Intended Audience :: Other Audience",
          "Intended Audience :: Science/Research",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Programming Language :: Python",
          "Programming Language :: Python :: 3",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Information Analysis",
          "Topic :: Scientific/Engineering :: Mathematics",
          "Topic :: Scientific/Engineering :: Visualization",
          "Topic :: Software Development :: Libraries",
          "Topic :: Utilities",
          ],

      author="Andreas Kloeckner",
      url="https://pypi.org/project/loopy",
      author_email="inform@tiker.net",
      license="MIT",

      install_requires=[
          "loopy>=2020.2",
          ],
      packages=find_packages())

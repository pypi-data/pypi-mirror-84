#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 17:39:15 2020

@author: uttiya
"""

import setuptools

#with open("README.md","r") as fh:
 #   long_description = fh.read()
    
setuptools.setup(
    name = "ebbp",
    version = "0.1",
    author = "Uttiya Maji",
    author_email = "iuttiya@gmail.com",
    description = "Empirical Bayes for the Binomial in Python",
  #  long_description = long_description,
   # long_description_content_type = "text/markdown",
    url = "https://github.com/uttiyamaji/ebbp",
    packages = setuptools.find_packages(),
    classifiers = ["Programming Language :: Python :: 3",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent"],
    python_requires = '>=3.6'
)


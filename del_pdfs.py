#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 02:36:02 2022

@author: sohanjs

"""

import os
import glob

files = glob.glob("*.pdf")

# Get the current working directory
cwd = os.getcwd()
print("Current working directory: {0}".format(cwd))

for f in files:
    os.system(f'rm -rf *.pdf')

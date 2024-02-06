"""
Authors: Morgan Jones and Alex Santos
Last Updated: 02/02/04

This file can be imported to change the working directory of executing code to the src directory. This stabilizes the paths of directories which import or output data files (such as processData.py).
"""

import os
src_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(src_dir)

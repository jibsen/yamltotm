#!/usr/bin/env python3

# Copyright (c) 2014 Joergen Ibsen
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Convert tmTheme plist to YAML.

Reads a file in tmTheme plist format used in TextMate and Sublime Text, and
outputs YAML format.

Note:
    Uses plistlib interface introduced in Python 3.4.
"""

import argparse
import plistlib

import yaml


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert tmTheme to YAML.')
    parser.add_argument('infile', type=argparse.FileType('rb'),
                        help='tmTheme scheme file')
    parser.add_argument('outfile', type=argparse.FileType('w'),
                        help='YAML scheme file')
    args = parser.parse_args()

    # read tmTheme plist and write YAML
    scheme = plistlib.load(args.infile)
    yaml.safe_dump(scheme, stream=args.outfile, default_flow_style=False)

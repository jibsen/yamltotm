#!/usr/bin/env python3

"""
Convert YAML to tmTheme format.

Reads a theme in YAML format and outputs tmTheme plist format used in
TextMate and Sublime Text.

Input files are concatenated.

An optional dictionary file (in YAML format), can be used to translate
strings.

Note: Uses plistlib interface introduced in Python 3.4.
"""

import argparse
import fileinput
import plistlib
import re
import yaml

userdict = {}

def dictrepl(matchobj):
    if matchobj.group(1) == '$':
        return '$'
    else:
        return userdict[matchobj.group(1)]

def str_constructor(loader, data):
    s = loader.construct_scalar(data)
    s = re.sub('\$(\$|\w+)', dictrepl, s)
    return s

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert YAML to tmTheme.')
    parser.add_argument('-d', '--dict', type=argparse.FileType('r'),
                        help='YAML dictionary file')
    parser.add_argument('infile', nargs='+', help='YAML theme file')
    parser.add_argument('outfile', type=argparse.FileType('wb'),
                        help='tmTheme theme file')
    args = parser.parse_args()

    # if user supplied a dictionary, read it and add our own constructor
    # for str objects that performs lookup
    if args.dict:
        userdict = yaml.safe_load(args.dict)
        yaml.add_constructor(u'tag:yaml.org,2002:str', str_constructor,
                             Loader=yaml.SafeLoader)

    # read YAML and write tmTheme plist
    with fileinput.input(args.infile) as f:
        theme = yaml.safe_load(''.join(f))
        plistlib.dump(theme, args.outfile)

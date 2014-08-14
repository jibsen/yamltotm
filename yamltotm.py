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
import collections
import plistlib
import re

import yaml


FileRange = collections.namedtuple('FileRange', 'lo hi name')


class MultiFile:
    """
    Array of lines from multiple files.
    """

    def __init__(self, filenames=None, mode='r'):
        self.lines = []
        self._files = []
        if filenames is not None:
            self.add_files(filenames, mode)

    def __iter__(self):
        return iter(self.lines)

    def add_files(self, filenames, mode='r'):
        """
        Add lines from files to end of MultiFile.

        :param filenames: List of filenames
        """
        base = len(self.lines)
        for name in filenames:
            with open(name, mode) as f:
                self.lines.extend(f.readlines())
                self._files.append(FileRange(base, len(self.lines), name))
                base = len(self.lines)

    def lookup_line(self, n):
        """
        Look up filename and line number from line index.

        :param n: Absolute index of line (starting at 0)
        :rtype: (str, int) or None
        :return: Filename and line number (starting at 1)
        """
        for f in self._files:
            if n >= f.lo and n < f.hi:
                return f.name, n - f.lo + 1
        else:
            return None


_mf = MultiFile()

_userdict = {}


def dictrepl(matchobj):
    if matchobj.group(1) == '$':
        return '$'
    else:
        return _userdict[matchobj.group(1)]


def str_constructor(loader, data):
    s = loader.construct_scalar(data)
    try:
        s = re.sub('\$(\$|\w+)', dictrepl, s)
    except KeyError as e:
        name, line = _mf.lookup_line(data.start_mark.line)
        print('KeyError in "{}", line {}:'.format(name, line), e)
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
        _userdict = yaml.safe_load(args.dict)
        yaml.add_constructor(u'tag:yaml.org,2002:str', str_constructor,
                             Loader=yaml.SafeLoader)

    # read YAML input files into MultiFile
    _mf.add_files(args.infile)

    # load YAML and write tmTheme plist
    try:
        theme = yaml.safe_load(''.join(_mf.lines))
    except yaml.YAMLError as e:
        if hasattr(e, 'problem_mark'):
            name, line = _mf.lookup_line(e.problem_mark.line)
            print('YAML error in "{}", line {}:'.format(name, line), e)
        else:
            print('YAML error:', e)
    else:
        plistlib.dump(theme, args.outfile)

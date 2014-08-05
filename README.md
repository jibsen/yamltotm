
YAML to tmTheme
===============

Color schemes for the [TextMate][] and [SublimeText][] editors (tmTheme files)
are stored as [plist][] XML, which is not the most human friendly format to
edit and maintain.

This project is an example of generating tmTheme files from [YAML][] sources
using a Python script. This has a number of advantages:

 - easy for humans to read and modify
 - little structural overhead
 - themes can be modularized
 - allows simple templating

[TextMate]: http://macromates.com/
[SublimeText]: http://www.sublimetext.com/
[plist]: http://developer.apple.com/documentation/Darwin/Reference/ManPages/man5/plist.5.html
[YAML]: http://yaml.org/


Usage
-----

`yamltotm.py` takes one or more YAML files and generates a tmTheme file. An
optional dictionary can be provided.

    usage: yamltotm.py [-h] [-d DICT] infile [infile ...] outfile

    Convert YAML to tmTheme.

    positional arguments:
      infile                YAML theme file
      outfile               tmTheme theme file

    optional arguments:
      -h, --help            show this help message and exit
      -d DICT, --dict DICT  YAML dictionary file

All input files are concatenated before they are processed, so it is important
to divide files in a way that maintains the structure of the content. For
tmTheme files this usually means keeping all top level keys in the first
file, ordered so `settings` is last. This way all further files go into
`settings`.

The dictionary is a YAML file mapping strings to their replacement. Any string
(key or value) in the input that fully matches a key in the dictionary will be
replaced with the corresponding value.

`tmtoyaml.py` converts a tmTheme file to YAML. The generated file is a simple
dump, but can serve as a starting point.


Example
-------

Given a theme file

```.yaml
name: __name__
uuid: __uuid__
settings:

# Editor settings
- settings:
    background: __blue__
    foreground: __white__

# Root groups
- name: Comment
  scope: comment
  settings:
    foreground: __gray__
```

and a dictionary

```.yaml
__name__: Simple Blue
__uuid__: e42124f9-7cf8-4477-ad7b-31a7f1050504
__blue__: '#0000FF'
__white__: '#FFFFFF'
__gray__: '#808080'
```

`yamltotm.py -d dict.yaml theme.yaml theme.tmTheme` will generate

```.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>name</key>
	<string>Simple Blue</string>
	<key>settings</key>
	<array>
		<dict>
			<key>settings</key>
			<dict>
				<key>background</key>
				<string>#0000FF</string>
				<key>foreground</key>
				<string>#FFFFFF</string>
			</dict>
		</dict>
		<dict>
			<key>name</key>
			<string>Comment</string>
			<key>scope</key>
			<string>comment</string>
			<key>settings</key>
			<dict>
				<key>foreground</key>
				<string>#808080</string>
			</dict>
		</dict>
	</array>
	<key>uuid</key>
	<string>e42124f9-7cf8-4477-ad7b-31a7f1050504</string>
</dict>
</plist>
```


License
-------

Copyright (c) 2014 Joergen Ibsen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

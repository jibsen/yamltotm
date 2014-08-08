
YAML to tmTheme
===============

Color themes for the [TextMate][] and [SublimeText][] editors (tmTheme files)
are stored as [plist][] XML, which is not the most human friendly format to
edit and maintain.

This project is an example of generating tmTheme files from [YAML][] sources
using a Python script. This has a number of advantages:

 - easy for humans to read and modify
 - little structural overhead
 - themes can be modularized
 - allows simple templating

Example themes:

 - [Solarized Minimal][solarmini]
 - [textmate-solarized][solartm] (example fork)
 - [SublimeColors/Solarized][solarst] (example fork)

[TextMate]: http://macromates.com/
[SublimeText]: http://www.sublimetext.com/
[plist]: http://developer.apple.com/documentation/Darwin/Reference/ManPages/man5/plist.5.html
[YAML]: http://yaml.org/
[solarmini]: https://github.com/jibsen/solarized_minimal
[solartm]: https://github.com/jibsen/textmate-solarized/tree/yamltotm_build
[solarst]: https://github.com/jibsen/Solarized/tree/yamltotm_build


Usage
-----

The scripts are written for Python 3, and use [PyYAML](http://pyyaml.org/).

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

The dictionary is a YAML file mapping identifiers to their replacement. In the
strings of the input file (both key and value), `$identifier` will be replaced
with the value of `identifier` in the dictionary. `$$` is an escape to insert
a literal `$`.

`tmtoyaml.py` converts a tmTheme file to YAML. The generated file is a simple
dump, but can serve as a starting point.


Example
-------

Given a theme file

```.yaml
name: $name
uuid: $uuid
settings:

# Editor settings
- settings:
    background: $blue
    foreground: $white

# Root groups
- name: Comment
  scope: comment
  settings:
    foreground: $gray
```

and a dictionary

```.yaml
name: Simple Blue
uuid: e42124f9-7cf8-4477-ad7b-31a7f1050504
blue: '#0000FF'
white: '#FFFFFF'
gray: '#808080'
```

`yamltotm.py -d dict.yaml theme.yaml theme.tmTheme` will generate

```.xml
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

This projected is licensed under the terms of the [MIT license](LICENSE).

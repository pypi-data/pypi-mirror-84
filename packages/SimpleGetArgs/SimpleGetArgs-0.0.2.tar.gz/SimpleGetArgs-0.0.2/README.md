# A project to simply check the publishing of the command Line
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![GitHub](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://raw.githubusercontent.com/mkfeuhrer/richest/master/LICENSE.txt)
[![PyPI version fury.io](https://badge.fury.io/py/richest.svg)](https://pypi.python.org/pypi/richest/)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

This repository teach my students to learn how to simply publish a python package with command line.
A Python package for getting list of numbers from 1 to 100 or saying hello to anyone, 

## Installation Instruction

- Chef-CLI is available as a python package.

- Open terminal and run ```pip install SimpleGetArgs```

- This installs the CLI app.

- Now run richest --help to know the available commands

- Enjoy !!

### Example

**To Print the numbers from 0 to 100**

```
GetArgs --counttill100
```

**To extract Top 20 Youngest Richest People**

```
GetArgs --print1 --name "NazGol"
```

**Complete option list**

```
richest -h
usage: richest [-h] [--current] [--youngest] [--oldest] [--male] [--female]

optional arguments:
  -h, --help      show this help message and exit
  --counttill100  Print count till 100
  --print1        Let you to Print Hello to any name
  --name NAME     Print Name
```

## Contributors

- [MSBeni](https://github.com/MSBeni)


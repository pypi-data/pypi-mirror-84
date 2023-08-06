PLTable
=======

![](https://camo.githubusercontent.com/65197dad277fbb4fecb852a4d8b14de9f2205c1d/68747470733a2f2f692e696d6775722e636f6d2f666870313676652e706e67)

PLTable is a Python library designed to make it quick and easy to represent tabular data in visually appealing text tables. PLTable is a fork of [PTable](https://github.com/kxxoling/PTable) which was in turn originally forked from [PrettyTable](https://github.com/lmaurits/prettytable) :

- [PrettyTable by Luke Maurits](https://github.com/lmaurits/prettytable)
  - [PTable by Kane Blueriver](https://github.com/kxxoling/PTable)
    - [PTable by Ryan James](https://github.com/Autoplectic/PTable/tree/boxchar)
      - [PLTable by Plato Mavropoulos](https://github.com/platomav/PLTable)

Compared to PTable, PLTable:

- Adds an improved Unicode line drawing table style based on Ryan James's original PTable fork, boxchar branch.
- Adds JSON Dictionary export via "get_json_dict" method. Convert it to JSON via python's built-in json import.
- Fixes HTML export via "get_html_string" by adding proper table Title/Caption and valid xHTML parameter toggle.

PLTable can be used as a drop-in replacement for PTable, provided that the module import name is changed accordingly. The opposite is not true because PLTable adds additional capabilities which are not present at PTable, while retaining the existing with bug fixes when necessary.

You can find the full PrettyTable documentation at the [PTable](https://ptable.readthedocs.io/en/latest/) or [PrettyTable](https://code.google.com/archive/p/prettytable/wikis) wikis.

To install PLTable, use pip via **pip install PLTable** or build from source via **python setup.py install**.
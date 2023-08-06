# Python Commons
[![PyPI version](https://badge.fury.io/py/drizm-commons.svg)](https://badge.fury.io/py/drizm-commons)  

This package includes shared code used by
the Drizm organizations development team.  

It is not intended for public usage but you
may still download, redistribute or 
modify it to your liking.

## Usage

Basic Install (utils only):  
>pip install drizm-commons


Full install (SQLAlchemy features available):  
>pip install drizm-commons[sqla]

Import like so:  
*import drizm_commons*

## Documentation

### Introspection

````python
from drizm_commons.inspect import SQLAIntrospector


table = SQLAIntrospector(my_table_instance)

""" Attributes """
table.tablename  # get the name of the table
table.classname  # get the classname of the declarative instance
table.columns  # get all SQLA fields of the class

""" Methods """
table.primary_keys()
table.primary_keys(retrieve_constraint=True)
````

## Changelog

### 0.1.1

- Added SQLAlchemy JSON Encoder
- Fixed bugs related to the Introspection
API
- Added table registry
- Added additional utilities

### 0.1.2

- Added get_root_path and recursive delete
Path utilities
- Fixed various bugs

### 0.2.0

- Added full test suite
- Added testing tools
- Revamped introspection API
- Provided additional overrides for the
SQL connection adapter

### 0.2.1

- Added support for datetime JSON
encoding

### 0.2.2

- Improved in-code documentation
- Integrated additional utils from
drizm-django-commons

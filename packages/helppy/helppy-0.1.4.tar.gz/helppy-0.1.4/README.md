[![PyPI version](https://badge.fury.io/py/helppy.svg?)](https://badge.fury.io/py/helppy)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/vvaezian/helppy/issues)
[![GitHub license](https://img.shields.io/github/license/vvaezian/helppy.svg)](https://github.com/vvaezian/helppy/blob/main/LICENCE)

If you have Python-related documention in GitHub, Helppy helps you to search for them without the need to leave your Python notebook.

## Installation
```python
pip install helppy
```

## Initializing
```python
from helppy import Helppy

hh = Helpy()
```

## Usage
Search the knowledge-base by providing a keyword that appears in the header of the sections in you documentation files, or search by providing a keyword that appears in your documentation files.  
In either case you can optionally provide a keyword for the files name to limit the search to those files.
```python
# Among all files that contain 'pandas' in their names, 
# print sections that their headers contain 'sql'
hh.find('sql', 'pandas')

# Among all files that contain 'pandas' in their names, 
# print the link of those files that contain 'sql' in their body.
hh.find(text_in_page='sql', subject='pandas')
```

There is a pre-built knowledge-base included in this package which uses my own documentations. To use your own repositories as the knowledge-base, you can 
1. Use the `refresh_kb(my_repo_url, extensions=['.md'])` function to load your repositories (lasts for the session).
2. After adding your repositories, save the knowledge-base to a file using `save_kb()` function, forke this repository, and replace the `kb.py` file with your file, and build a new package.

Any GitHub path can be used for building the knowledge-base, doesn't have to be a repository path. 

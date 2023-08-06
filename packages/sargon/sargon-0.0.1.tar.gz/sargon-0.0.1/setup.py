# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sargon']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sargon',
    'version': '0.0.1',
    'description': 'A random generator of codes, names and other words',
    'long_description': '# Sargon: Random Code Generator\n\n`sargon` is a simple Python package (no external dependencies) to generate random (mnemonic) codes simulating Youtube or Heroku style. It\'s extensible to define your own rules too.\n\n### Basic usage\n\n#### Heroku\n\n`heroku(code_length=4)`\n\nHeroku codes have the form `ADJECTIVE-NOUN-CODE`:\n\nExample:\n\n```python\n>>> from sargon import heroku\n>>> heroku()\n"valuable-period-6016"\n\n>>> heroku(6)\n"sweet-hat-673004"\n```\n\n#### YouTube\n\n`youtube(length=11, avoid_confusing_chars=False, blacklist_symbols=None)`\n\nExample:\n\n```python\n>>> from sargon import youtube\n>>> youtube()\n"dQw4w9WgXcQ"\n\n>>> youtube(6)\n"LNb-P0"\n\n>>> youtube(6, blacklist_symbols=\'-\')\n"LNbP0X"\n```\n\n#### 6 Digit Generator\n\n`six_digit()`\n\n```python\n>>> from sargon import six_digit\n>>> six_digit()\n"770584"\n```\n\n### Defining your own generators\n\nCheckout `engines.py` for the list of available engines and the parameters they receive. Here\'s an example:\n\n```python\n>>> from sargon import engines, build_generator\n>>> generator = build_generator(\n    engines.CityWordEngine(country=\'United States\'),\n    engines.NumberEngine(4))\n>>> generator.generate()\n"bellview-5269"\n```\n\n### Why `sargon`?\n\nI wanted to call the package [Hammurabi](https://en.wikipedia.org/wiki/Hammurabi), as the babylonian king that issued the [Code of Hammurabi](https://en.wikipedia.org/wiki/Code_of_Hammurabi), but there\'s another package named `hammurabi`, so I went with another great ruler that I like to read about: [Sargon the great](https://en.wikipedia.org/wiki/Sargon_of_Akkad) the emperor of the Akkadian empire, what is thought today to be the first empire in history.\n',
    'author': 'Santiago Basulto',
    'author_email': 'santiago.basulto@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/santiagobasulto/sargon',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

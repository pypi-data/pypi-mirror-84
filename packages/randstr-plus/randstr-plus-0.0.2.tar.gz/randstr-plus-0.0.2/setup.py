# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['randstr_plus']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'randstr-plus',
    'version': '0.0.2',
    'description': 'A more flexible string generator',
    'long_description': '<h1 align="center">randstr-plus</h1>\n<h3 align="center">A slightly more flexible string generator</h3>\n<p align="center">\n  <a href="https://github.com/garytyler/randstr-plus/actions">\n    <img alt="Actions Status" src="https://github.com/garytyler/randstr-plus/workflows/tests/badge.svg">\n  </a>\n\n  <a href="https://codecov.io/gh/garytyler/randstr-plus">\n    <img src="https://codecov.io/gh/garytyler/randstr-plus/branch/master/graph/badge.svg?token=3N9UKA0AHY" />\n  </a>\n  <a href="https://pypi.org/project/randstr-plus/">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/randstr-plus">\n  </a>\n  <a href="https://pypi.org/project/randstr-plus/">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/randstr-plus">\n  </a>\n  <img alt="GitHub" src="https://img.shields.io/github/license/garytyler/randstr-plus">\n  <a href="https://github.com/psf/black">\n    <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n  </a>\n</p>\n\n## Functions\n\n<td style="color: #444;">\n  <dl style="color: #666;">\n    <dt><a name="-randstr"><h4><b>randstr</b></a>(min_length: int = 5, max_length: int =\n      25, min_tokens: int = 1, max_tokens: int = 5, lowercase_letters: bool = True,\n      uppercase_letters: bool = True, punctuation: bool = True, numbers: bool = True) -&gt;\n      str<h4></dt>\n    <dd><h5>Return&nbsp;a&nbsp;single&nbsp;string&nbsp;generated&nbsp;from&nbsp;random&nbsp;characters&nbsp;according&nbsp;to&nbsp;the&nbsp;given&nbsp;parameters.<br>\n        &nbsp;<br>\n        Keyword&nbsp;Arguments:<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;min_length&nbsp;{int}&nbsp;--&nbsp;minimum&nbsp;total&nbsp;character&nbsp;length&nbsp;(default:&nbsp;{5})<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;max_length&nbsp;{int}&nbsp;--&nbsp;maximum&nbsp;total&nbsp;character&nbsp;length&nbsp;&nbsp;(default:&nbsp;{25})<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;min_tokens&nbsp;{int}&nbsp;--&nbsp;minimum&nbsp;total&nbsp;tokens/words&nbsp;(default:&nbsp;{1})<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;max_tokens&nbsp;{int}&nbsp;--&nbsp;maximum&nbsp;total&nbsp;tokens/words&nbsp;(default:&nbsp;{5})<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;lowercase_letters&nbsp;{bool}&nbsp;--&nbsp;allow&nbsp;lowercase&nbsp;letters&nbsp;(default:&nbsp;{True})<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;uppercase_letters&nbsp;{bool}&nbsp;--&nbsp;allow&nbsp;uppercase&nbsp;letters&nbsp;(default:&nbsp;{True})<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;punctuation&nbsp;{bool}&nbsp;--&nbsp;allow&nbsp;punctuation&nbsp;characters&nbsp;(default:&nbsp;{True})<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;numbers&nbsp;{bool}&nbsp;--&nbsp;allow&nbsp;numbers&nbsp;(default:&nbsp;{True})<br>\n        &nbsp;<br>\n        Returns:<br>\n        &nbsp;&nbsp;&nbsp;&nbsp;str&nbsp;--&nbsp;generated&nbsp;string</h5></dd>\n  </dl>\n</td>\n',
    'author': 'Gary Tyler',
    'author_email': 'mail@garytyler.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/garytyler/randstr-plus',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

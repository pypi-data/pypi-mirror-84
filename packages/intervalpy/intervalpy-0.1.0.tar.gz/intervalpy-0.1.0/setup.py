# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intervalpy']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.9,<0.10']

entry_points = \
{'console_scripts': ['test = pytest:main']}

setup_kwargs = {
    'name': 'intervalpy',
    'version': '0.1.0',
    'description': 'An interval set utility library.',
    'long_description': '# intervalpy\n\n![Tests](https://github.com/diatche/intervalpy/workflows/Tests/badge.svg)\n\nAn interval set utility library.\n\n# Installation\n\nWith [poetry](https://python-poetry.org):\n\n```bash\npoetry add intervalpy\n```\n\nOr with pip:\n\n```\npip3 install intervalpy\n```\n\n# Usage\n\nHave a look at the [documentation](https://diatche.github.io/intervalpy/).\n\nBasic usage:\n\n```python\nfrom interval_util import Interval\n\ndigits = Interval(0, 10, end_open=True)\nten_and_up = digits.get_gt()\npositive_numbers = digits.get_gte()\nassert ten_and_up.is_subset_of(positive_numbers)\n\nassert positive_numbers.intersection(Interval.lt(10)) == digits\n```\n',
    'author': 'Pavel Diatchenko',
    'author_email': 'diatche@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/diatche/intervalpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4',
}


setup(**setup_kwargs)

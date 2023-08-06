# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pipen', 'pipen.channel']

package_data = \
{'': ['*']}

install_requires = \
['cached-property>=1.0.0,<2.0.0',
 'diot',
 'enlighten>=1.0.0,<2.0.0',
 'liquidpy',
 'more-itertools>=8.0.0,<9.0.0',
 'pandas>=1.0.0,<2.0.0',
 'pyparam',
 'python-simpleconf',
 'python-slugify>=4.0.0,<5.0.0',
 'rich>=9.0.0,<10.0.0',
 'simplug',
 'siuba<1.0.0',
 'toml>=0.10,<0.11',
 'uvloop<1.0.0',
 'varname',
 'xqute']

entry_points = \
{'console_scripts': ['pipen = pipen.cli:main']}

setup_kwargs = {
    'name': 'pipen',
    'version': '0.0.0',
    'description': 'A pipeline framework for python',
    'long_description': '# pipen - A pipeline framework for python\n\n[![Pypi][1]][2] [![Github][3]][4] [![PythonVers][5]][2] [![docs][6]][7] [![building][8]][7] [![Codacy][9]][10] [![Codacy coverage][11]][10]\n\n[Documentation][7] | [API][11] | [Change log][12]\n\n## Installation\n```bash\npip install -U pipen\n```\n\n\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pipen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

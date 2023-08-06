# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['u_coreutils',
 'u_coreutils.cat',
 'u_coreutils.echo',
 'u_coreutils.false',
 'u_coreutils.head',
 'u_coreutils.mkdir']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['u-cat = u_coreutils.cat:run',
                     'u-echo = u_coreutils.echo:run',
                     'u-false = u_coreutils.false:run',
                     'u-head = u_coreutils.head:run',
                     'u-mkdir = u_coreutils.mkdir:run']}

setup_kwargs = {
    'name': 'u-coreutils',
    'version': '0.1.8',
    'description': 'GNU coreutils implementation with Python 3.8',
    'long_description': "# u-coreutils\n\n![CI](https://github.com/duyixian1234/u-coreutils/workflows/CI/badge.svg?branch=master)\n\nGNU coreutils implementation with Python 3.8\n\n## Tools\n\n✔ cat\n\n✔ echo\n\n✔ head\n\n✔ mkdir\n\n## INSTALL\n\n```shell\npip install -U u_coreutils\n```\n\n## USE\n\n```shell\nu-cat a.txt\nu-echo -e -n 'Hello,World!\\n'\nu-head -n 5 a.txt\nu-mkdir -p -v a/b/c/d\n```\n",
    'author': 'duyixian',
    'author_email': 'duyixian1234@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/duyixian1234/u-coreutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

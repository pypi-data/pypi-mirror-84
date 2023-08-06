# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['literotica_dl', 'literotica_dl.classes']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['literotica_dl = literotica_dl.__main__:main']}

setup_kwargs = {
    'name': 'literotica-dl',
    'version': '0.0.1',
    'description': 'A tool to download stories from Literotica',
    'long_description': '# literotica_dl\n\n# Credits\n\nThis package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [fuzzyfiend/pythoncookie](https://github.com/fuzzyfiend/pythoncookie) project template.\n',
    'author': 'FuzzyFiend',
    'author_email': '50032576+fuzzyfiend@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fuzzyfiend/literotica_dl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)

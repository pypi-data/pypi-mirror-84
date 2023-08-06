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
    'version': '0.0.2',
    'description': 'A tool to download stories from Literotica',
    'long_description': '# literotica_dl\nA tool to download stories from Literotica.\n\nYou must specify whether to download stories (-s) or author works (-a).\n* Stories are identified as the url stub following the /s/ directory in the url\n    * https://www.literotica.com/s/a-my-name-is-alice\n    * story flag is a-my-name-is-alice\n* Authors are identified as the memberuid\n    * https://www.literotica.com/stories/memberpage.php?uid=36374\n    * author flag is 36374\n\nThis program will attempt to resolve the author uid or story id for you.\nBy default this program will write stories to a new folder called output. This can be overridden by specifying the -o flag.\n\n# Examples\n```sh\n# Downloading an authors works via the author stub\nliterotica_dl -a 36374\n\n# Downloading an authors works via member url\nliterotica_dl -a "https://www.literotica.com/stories/memberpage.php?uid=36374"\n\n# Downloading an story via the story stub\nliterotica_dl -s a-my-name-is-alice\n\n# Downloading an story via the story stub\nliterotica_dl -s "https://www.literotica.com/s/a-my-name-is-alice"\n\n# Mirroring the author to a specific directory\nliterotica_dl -a "https://www.literotica.com/stories/memberpage.php?uid=36374" -o "archive"\n```\n\n# Credits\n\nThis package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [fuzzyfiend/pythoncookie](https://github.com/fuzzyfiend/pythoncookie) project template.\n',
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['espyta']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.0,<0.11.0', 'tornado>=6.0,<7.0']

entry_points = \
{'console_scripts': ['espyta = espyta.__main__:main']}

setup_kwargs = {
    'name': 'espyta',
    'version': '0.0.0',
    'description': 'Webhook handler to flash ESPs through OTA.',
    'long_description': '# espyta\n\nThis software provides a webhook handler to automatically flash any ESP-based\ndevices on your network when the repository for their firmware gets updated.\n\n## Requirements\n\n- Python 3.6 or up.\n- [PlatformIO Core (CLI)](https://docs.platformio.org/en/latest/core/) 5.0 or up.\n\n## Installation\n\nI recommend you use a virtual environment and use that to install `espyta`. You\ncan then start the `espyta` HTTP server as follows:\n\n```\n# python3.8 -m venv venv\n# venv/bin/pip install espyta\n# venv/bin/espyta http\n```\n\n## Configuration\n\n## Documentation\n\nYou can read more on our full [documentation website](https://espyta.readthedocs.io/en/latest/).\n',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supakeen/espyta',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)

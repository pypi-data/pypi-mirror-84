# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notify', 'notify.linux', 'notify.win32']

package_data = \
{'': ['*']}

extras_require = \
{':sys_platform == "linux"': ['pycairo>=1.18.1,<2.0.0',
                              'PyGObject>=3.34.0,<4.0.0'],
 ':sys_platform == "win32"': ['pypiwin32==223', 'pywin32==228']}

setup_kwargs = {
    'name': 'notify-send',
    'version': '0.0.16',
    'description': 'Displays a notification suitable for the platform being run on.',
    'long_description': "# notify-send\n\n![](header.png)\n\n## Installation\n\n```sh\n    pip install notify-send\n```\n\n## Usage example\n\n```python\n    from notify import notification\n    notification('body message', title='optinal')\n```\n\n## Development setup\n\n```sh\n    git clone https://github.com/andreztz/notify-send.git\n    cd notify-send\n    virtualenv venv\n    source venv/bin/activate\n    pip install -e .\n```\n\n## Release History\n\n-   0.0.16 - The first proper release\n    -   Work in progress\n\n## Meta\n\nAndré P. Santos – [@ztzandre](https://twitter.com/ztzandre) – andreztz@gmail.com\n\nDistributed under the MIT license. See `LICENSE` for more information.\n\n[https://github.com/andreztz/notify-send](https://github.com/andreztz/)\n\n## Contributing\n\n1. Fork it (<https://github.com/andreztz/notify-send/fork>)\n2. Create your feature branch (`git checkout -b feature/fooBar`)\n3. Commit your changes (`git commit -am 'Add some fooBar'`)\n4. Push to the branch (`git push origin feature/fooBar`)\n5. Create a new Pull Request\n",
    'author': 'André P. Santos',
    'author_email': 'andreztz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andreztz/notify-send',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

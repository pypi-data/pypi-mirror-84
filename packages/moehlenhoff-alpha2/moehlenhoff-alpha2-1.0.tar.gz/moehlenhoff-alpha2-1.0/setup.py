# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['moehlenhoff_alpha2']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.2,<4.0.0', 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'moehlenhoff-alpha2',
    'version': '1.0',
    'description': 'Python client for the Moehlenhoff Alpha2 underfloor heating system',
    'long_description': '# python-moehlenhoff-alpha2\nPython client for the Moehlenhoff Alpha2 underfloor heating system\n\n## Installation\n\nMoehlenhoff Alpha2 can be installed from PyPI using `pip` or your package manager of choice:\n\n``` bash\npip install moehlenhoff-alpha2\n```\n\n## Usage example\n\n``` python\nimport asyncio\nfrom moehlenhoff_alpha2 import Alpha2Base\n\nasync def main():\n    base = Alpha2Base("192.168.1.1")\n    await base.update_data()\n    ha = list(base.heatareas)[0]\n    t_target = ha["T_TARGET"] + 0.2\n    await base.update_heatarea(ha["ID"], {"T_TARGET": t_target})\n\nasyncio.run(main())\n```\n',
    'author': 'Jan Schneider',
    'author_email': 'oss@janschneider.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/j-a-n/python-moehlenhoff-alpha2',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

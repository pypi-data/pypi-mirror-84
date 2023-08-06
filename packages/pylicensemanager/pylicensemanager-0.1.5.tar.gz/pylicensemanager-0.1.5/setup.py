# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylicensemanager']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'pylicensemanager',
    'version': '0.1.5',
    'description': 'PyLicenseManager is a Python client library for the License Manager for Woocommerce Rest API.',
    'long_description': '# Pylicensemanager\n\nPyLicenseManager is a Python client library for the License Manager for Woocommerce Rest API.\n\n## Installation\n\nUse the package manager [pip](https://pypi.org/) to install pylicensemanager.\n\n`\npip install pylicensemanager\n`\n\n## Usage\n\n```\nimport pylicensemanager\n```\n\nReview documentation for more information: https://www.licensemanager.at/docs/rest-api/\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n[MIT](https://choosealicense.com/licenses/mit/)',
    'author': 'Michael Ramsey',
    'author_email': 'mike@hackerdise.me',
    'maintainer': 'Michael Ramsey',
    'maintainer_email': 'mike@hackerdise.me',
    'url': 'https://www.licensemanager.at/docs/rest-api/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octoapi']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=3.2.1,<4.0.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'pytz>=2020.4,<2021.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'octoapi',
    'version': '0.1.0',
    'description': 'Python interface to Octopus Energy API',
    'long_description': '![OctoAPI Logo](docs/_static/logo.png)\n\n[![Coverage Status](https://coveralls.io/repos/github/jemrobinson/octoapi/badge.svg?branch=main)](https://coveralls.io/github/jemrobinson/octoapi?branch=main)\n[![Dependabot](https://flat.badgen.net/dependabot/jemrobinson/octoapi?icon=dependabot)](https://dependabot.com/)\n[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Licence: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)\n[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)\n\n[![Build Status](https://travis-ci.com/jemrobinson/octoapi.svg?branch=main)](https://travis-ci.com/jemrobinson/octoapi)\n![OSX](https://img.shields.io/badge/-555?&logo=apple&logoColor=white)[![Build Status](https://badges.formidable.com/travis.com/jemrobinson/octoapi?branch=main&env=OSBADGE=osx&label=%20)](https://travis-ci.com/github/jemrobinson/octoapi)\n![Linux](https://img.shields.io/badge/-555?&logo=linux&logoColor=white)[![Build Status](https://badges.formidable.com/travis.com/jemrobinson/octoapi?branch=main&env=OSBADGE=linux&label=%20)](https://travis-ci.com/github/jemrobinson/octoapi)\n![Windows](https://img.shields.io/badge/-555?&logo=windows&logoColor=white)[![Build Status](https://badges.formidable.com/travis.com/jemrobinson/octoapi?branch=main&env=OSBADGE=windows&label=%20)](https://travis-ci.com/github/jemrobinson/octoapi)\n\n## OctoAPI\nThis package provides a Python interface to the [Octopus Energy API](https://developer.octopus.energy/docs/api/).\n\n#### Dependencies\n- `Python >= 3.6`\n\n#### Install\nWIP\n<!-- Install with `pip` using\n\n```bash\npip install octoapi\n``` -->\n\n#### Deploy\nWIP\n\n#### Testing\nThe automated tests can be run using\n\n```bash\npytest\n```\n\n## Contribute\nPlease look at [our contributing guidelines](CONTRIBUTING.md) if you want to contribute to this project. GitHub also has some good guides on [how to contribute](https://guides.github.com/activities/contributing-to-open-source/#contributing).\n\n## License\nThis project uses a [GPL v3 licence](LICENSE).\n',
    'author': 'James Robinson',
    'author_email': 'james.em.robinson@gmail.com',
    'maintainer': 'James Robinson',
    'maintainer_email': 'james.em.robinson@gmail.com',
    'url': 'https://github.com/jemrobinson/octoapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dhis2',
 'dhis2.core',
 'dhis2.core.metadata',
 'dhis2.core.metadata.models',
 'dhis2.generate',
 'dhis2.openhie',
 'dhis2.openhie.resources']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'fhir.resources>=5.1.1,<6.0.0',
 'pydantic>=1.7.2,<2.0.0',
 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['dhis2 = dhis2.__main__:main']}

setup_kwargs = {
    'name': 'dhis2',
    'version': '0.2.1',
    'description': 'Tool for working and integrating with dhis2 instances',
    'long_description': '# dhis2-python: integration client for dhis2\n\n[![Package version](https://badge.fury.io/py/dhis2.svg)](https://pypi.python.org/pypi/dhis2)\n\n**Requirements**: Python 3.8+\n\n## Quickstart\n\nInstall using `pip`:\n\n```shell\n$ pip install dhis2\n```\n\nThis will install the `dhis2` command in your local environment (installing into a virtual environment recommended).\n\nThe tool supports a pluggable architecture, but the core supports:\n\n* Inspecting dhis2 instances\n    * `dhis2 -i inventory.yml inspect host-id/group-id`\n* Extracting mCSD and SVCM compatible payload, and pushing those to a FHIR compliant server\n    * `dhis2 -i inventory.yml openhie mcsd mcsd-config.yml`\n    * `dhis2 -i inventory.yml openhie svcm svcm-config.yml`\n\n(see description of formats below)\n\nAs of now, we do not support sending data to dhis2, only extraction is supported.\n\n## Formats\n\n### Inventory\n\nThe inventory is where you will store all your services, and various groupings you might find useful (most commands will only work on single sources/targets though, with the exception of the `inspect` command currently)\n\nThe basic format is as follows\n\n```yaml\nhosts:\n  playdev:\n    type: dhis2\n    baseUrl: https://play.dhis2.org/dev\n    username: admin\n    password: district\n  playdemo:\n    type: dhis2\n    baseUrl: https://play.dhis2.org/demo\n    auth:\n      default:\n        type: http-basic\n        username: admin\n        password: district\n  fhirdemo:\n    type: fhir\n    baseUrl: http://localhost:8080\ngroups:\n  dhis2:\n    - playdev\n    - playdemo\n```\n\nThe keys of the `hosts` and `groups` block will be used to identifiy targets when using the `dhis2` commands.\n\nPlease note that:\n\n* Currently only `http-basic` is supported for dhis2\n* For fhir no authentication is supported (coming soon)\n\n### mCSD / SVCM configuration\n\nBoth mCSD and SVCM currently has the exact same format so we will describe them together. You will need a source host, target host (or some other target) and a set of filters if desired.\n\nBasic format\n\n```yaml\nsource:\n  id: playdev\ntarget:\n  id: fhirdemo\n```\n\nThis configuration would simply take all org unit or option sets inside of dhis2 and push them to a fhir instance.\n\nIf you would want to store the result instead, you can use the `log://` target\n\n```yaml\nsource:\n  id: playdev\ntarget:\n  id: log://\n\n```\n\n(this is also the default if no target is given)\n',
    'author': 'Morten Hansen',
    'author_email': 'morten@dhis2.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dhis2/dhis2-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

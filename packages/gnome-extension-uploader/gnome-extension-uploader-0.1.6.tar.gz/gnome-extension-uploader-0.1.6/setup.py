# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gnome_extension_uploader']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.24.0,<3.0.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['geu = gnome_extension_uploader.cli:app']}

setup_kwargs = {
    'name': 'gnome-extension-uploader',
    'version': '0.1.6',
    'description': '',
    'long_description': '# Gnome Extension Uploader\nTool to upload Gnome-Shell extensions to [extensions.gnome.org](https://extensions.gnome.org).\n\n## Install\n```console\npip install gnome-extension-uploader\n```\n\n## How to use\n```console\ngeu build # runs glib-compile-schemas and builds the zip file\ngeu publish --username <YOUR_EXTENSIONS_GNOME_ORG_USERNAME> --password <YOUR_EXTENSIONS_GNOME_ORG_PASSWORD>\ngeu --help # for help :)\n```\n\nYou can also provide your username and password via environment variables (GEU_USERNAME, GEU_PASSWORD).\n\n## Use in Gitlab CI/CD\nAdd GEU_USERNAME and GEU_PASSWORD to your build variables in your repository settings.\n\nThis will publish every tag on [extensions.gnome.org](https://extensions.gnome.org)\n```yaml\nstages:\n  - publish\n\nproduction:\n  image: python:3.8.3-buster\n  stage: publish\n  script:\n    - pip install gnome-extension-uploader\n    - geu publish\n  only:\n    - tags\n```\n\n## Support\nFeel free to submit a pull request or consider making a donation on [Flatter](https://flattr.com/@SebastianNoelLuebke).',
    'author': 'Sebastian Noel Lübke',
    'author_email': 'sebastian@luebke.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebastianLuebke/gnome-extension-uploader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

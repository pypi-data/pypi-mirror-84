# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tbdebug', 'tbdump', 'tbpeep']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.3,<0.4.0', 'peepshow>=0.2.3,<0.3.0']

entry_points = \
{'console_scripts': ['tbdump = tbdump.__main__:tbdump',
                     'tbload = tbdump.__main__:tbload',
                     'tbpeep = tbdump.__main__:tbpeep']}

setup_kwargs = {
    'name': 'tibidi',
    'version': '0.1.0',
    'description': 'Dump your traceback into a file.',
    'long_description': '# tbdump\n\nDump your traceback into a file.\n\n* Documentation: <https://gergelyk.github.io/python-tbdump>\n* Repository: <https://github.com/gergelyk/python-tbdump>\n* Package: <https://pypi.python.org/pypi/tbdump>\n* Author: [Grzegorz Krasoń](mailto:grzegorz.krason@gmail.com)\n* License: [MIT](LICENSE)\n\n## Requirements\n\nThis package requires CPython 3.8 or compatible. If you have other version already installed, you can switch using `pyenv`. It must be installed as described in the [manual](https://github.com/pyenv/pyenv).\n\n```sh\npyenv install 3.8.2\npyenv local 3.8.2\n```\n\n## Installation\n\n```sh\npip install tbdump\n```\n\n## Usage\n\n```sh\npoetry run python tbdump/hello.py\n```\n\n## Development\n\n```sh\n# Preparing environment\npip install --user poetry  # unless already installed\npoetry install\n\n# Auto-formatting\npoetry run docformatter -ri tbdump tests\npoetry run isort -rc tbdump tests\npoetry run yapf -r -i tbdump tests\n\n# Checking coding style\npoetry run flake8 tbdump tests\n\n# Checking composition and quality\npoetry run vulture tbdump tests\npoetry run mypy tbdump tests\npoetry run pylint tbdump tests\npoetry run bandit tbdump tests\npoetry run radon cc tbdump tests\npoetry run radon mi tbdump tests\n\n# Testing with coverage\npoetry run pytest --cov tbdump --cov tests\n\n# Rendering documentation\npoetry run mkdocs serve\n\n# Building package\npoetry build\n\n# Releasing\npoetry version minor  # increment selected component\ngit commit -am "bump version"\ngit push\ngit tag ${$(poetry version)[2]}\ngit push --tags\npoetry build\npoetry publish\npoetry run mkdocs build\npoetry run mkdocs gh-deploy -b gh-pages\n```\n\n## Donations\n\nIf you find this software useful and you would like to repay author\'s efforts you are welcome to use following button:\n\n[![Donate](https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url)\n\n',
    'author': 'Grzegorz Krasoń',
    'author_email': 'grzegorz.krason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gergelyk.github.io/python-tbdump',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

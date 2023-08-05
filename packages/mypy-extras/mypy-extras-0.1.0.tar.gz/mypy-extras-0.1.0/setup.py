# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mypy_extras',
 'mypy_extras.plugin',
 'mypy_extras.plugin.features',
 'mypy_extras.plugin.typeops']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mypy-extras',
    'version': '0.1.0',
    'description': 'A collection of extra types and features for mypy',
    'long_description': '# mypy-extras\n\n[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services)\n[![test](https://github.com/wemake-services/mypy-extras/workflows/test/badge.svg?branch=master&event=push)](https://github.com/wemake-services/mypy-extras/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/wemake-server/mypy-extras/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake-server/mypy-extras)\n[![Python Version](https://img.shields.io/pypi/pyversions/mypy-extras.svg)](https://pypi.org/project/mypy-extras/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\n\n## Features\n\n- Provides a custom `mypy` plugin to enhance its possibilities\n- Provides new types that can be used in your programs with our plugin\n- Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n\n\n## Installation\n\n```bash\npip install mypy-extras\n```\n\nYou also need to [configure](https://mypy.readthedocs.io/en/stable/config_file.html)\n`mypy` correctly and install our custom plugin:\n\n```ini\n# In setup.cfg or mypy.ini:\n[mypy]\nplugins =\n  mypy_extras.plugin.entrypoint\n```\n\nWe also recommend to use the same `mypy` settings [we use](https://github.com/wemake-services/wemake-python-styleguide/blob/master/styles/mypy.toml).\n\n\n## Usage\n\n### AttrOf\n\nWe provide a special type to get named attributes of other types, like so:\n\n```python\nfrom typing_extensions import Literal  # or typing on python3.8+\nfrom mypy_extras import AttrOf\n\nclass User(object):\n    def auth(self, username: str, password: str) -> bool:\n        return False  # Just an example\n\ndef get_callback(user: User) -> AttrOf[User, Literal[\'auth\']]:\n    return user.auth\n\nuser: User\nreveal_type(get_callback(user))\n# Revealed type is \'def (username: builtins.str, password: builtins.str) -> builtins.bool\'\n```\n\n\n### ensure_attr\n\nWe can ensure that some `str` attribute exists on a object:\n\n```python\nfrom mypy_extras import ensure_attr\n\n\nclass User(object):\n    policy = \'update\'\n\n\nreveal_type(ensure_attr(User, \'policy\'))  # Revealed type is \'Literal[\'policy\']\'\nreveal_type(ensure_attr(User, \'missing\'))  # Error: attribute "missing" does not exist on type "User"\n```\n\nIt is useful when we do any manipulations with objects based on a string field:\n\n```python\nDEFAULT_POLICY_FIELD: Final = ensure_attr(User, \'policy\')  # typesafe\n# vs\nDEFAULT_POLICY_FIELD: Final = \'policy\'  \n# User can rename the field, and this will blow now!\n```\n\n\n## License\n\n[MIT](https://github.com/wemake.services/mypy-extras/blob/master/LICENSE)\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wemake.services/mypy-extras',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)

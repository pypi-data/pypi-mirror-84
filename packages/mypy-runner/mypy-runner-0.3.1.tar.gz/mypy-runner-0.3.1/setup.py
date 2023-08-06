# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mypyrun']
install_requires = \
['configparser']

extras_require = \
{'tests': ['pytest>=6.1,<7.0', 'coverage']}

entry_points = \
{'console_scripts': ['mypyrun = mypyrun:main']}

setup_kwargs = {
    'name': 'mypy-runner',
    'version': '0.3.1',
    'description': 'Run mypy with options to filter errors and colorize output',
    'long_description': "mypy-runner\n===========\n\nEase your way into static type checking by focusing on a small set of problems at a time.\n\nIt can be quite challenging to get an existing code base to pass mypy's checks, even at its most lenient settings, and unfortunately, until you do you can't use mypy as part of your CI/CD process.\n\n``mypy-runner`` lets you gradually introduce type checking by identifying a subset of files and errors to check:\n\n- choose a set of files and errors to check\n- get tests passing and enforce them in your CI and pre-commit hooks\n- repeat\n\nFeatures\n--------\n\n``mypy-runner`` adds the following features to ``mypy``:\n\n- Display colorized output\n- Convert specific errors to warnings\n- Filter specific errors and warnings\n\nCompatibility\n-------------\n\n``mypy-runner`` supports ``mypy`` 0.730 and higher.\n\nOptions\n-------\n\n::\n\n    usage: mypyrun.py [-h] [--version] [--daemon] [--select SELECT [SELECT ...]]\n                      [--ignore IGNORE [IGNORE ...]] [--warn WARN [WARN ...]]\n                      [--color] [--show-ignored] [--options OPTIONS]\n                      [--config-file CONFIG_FILE] [--files FILES [FILES ...]]\n                      [--warning-filters WARNING_FILTERS [WARNING_FILTERS ...]]\n                      [--error-filters ERROR_FILTERS [ERROR_FILTERS ...]]\n                      [--mypy-executable MYPY_EXECUTABLE]\n                      [ARG [ARG ...]]\n\n    positional arguments:\n      ARG                   Regular mypy flags and files (precede with --)\n\n    optional arguments:\n      -h, --help            show this help message and exit\n      --version             show program's version number and exit\n      --daemon              Run mypy in daemon mode (inverse: --no-daemon)\n      --select SELECT [SELECT ...], -s SELECT [SELECT ...]\n                            Errors to check\n      --ignore IGNORE [IGNORE ...], -i IGNORE [IGNORE ...]\n                            Errors to skip\n      --warn WARN [WARN ...], -w WARN [WARN ...]\n                            Errors to convert into warnings\n      --color               Colorize output (inverse: --no-color)\n      --show-ignored, -x    Show errors that have been ignored (darker if using\n                            color)\n      --options OPTIONS, -o OPTIONS\n                            Override the default options to use the\n                            namedconfiguration section (e.g. pass --options=foo to\n                            use the [mypyrun-foo] section)\n      --config-file CONFIG_FILE, -c CONFIG_FILE\n                            Specific configuration file.\n      --files FILES [FILES ...]\n                            Files to isolate (triggers use of 'active'options for\n                            these files)\n      --warning-filters WARNING_FILTERS [WARNING_FILTERS ...]\n                            Regular expression to ignore messages flagged as\n                            warnings\n      --error-filters ERROR_FILTERS [ERROR_FILTERS ...]\n                            Regular expression to ignore messages flagged as\n                            errors\n      --mypy-executable MYPY_EXECUTABLE\n                            Path to the mypy executable\n\nAs with tools like ``flake8``, you use specific error codes to enable or disable error output.\nErrors that are ignored or converted into warnings will not trigger a non-zero exit status.\n\nConfiguration\n-------------\n\n``mypyrun`` looks for a ``[mypyrun]`` section in either ``mypy.ini`` or ``mypyrun.ini``.\n\nHere's an example configuration file:\n\n.. code-block:: ini\n\n    [mypyrun]\n\n    # run dmypy instead of mypy\n    daemon = true\n\n    # only display these errors\n    select =\n        not_defined,\n        return_expected,\n        return_not_expected,\n        incompatible_subclass_attr,\n\n    # all other errors are warnings\n    warn = *\n\n    # filter errors generated from these paths:\n    exclude =\n        thirdparty/*,\n\n    # pass these paths to mypy\n    paths =\n        arnold/python,\n        houdini/python,\n        katana/python,\n        mari/python,\n        maya/python,\n        nuke/python,\n        python/packages,\n",
    'author': 'Chad Dombrova',
    'author_email': 'chadrik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chadrik/mypy-runner',
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
}


setup(**setup_kwargs)

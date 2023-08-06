# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peepshow',
 'peepshow.cmds',
 'peepshow.core',
 'peepshow.pager',
 'peepshow.utils']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.8.1,<0.9.0',
 'astunparse>=1.6.3,<2.0.0',
 'colorama>=0.4.4,<0.5.0',
 'getch>=1.0,<2.0',
 'miscutils>=1.4.0,<2.0.0',
 'pprintpp>=0.4.0,<0.5.0',
 'pygments>=2.7.2,<3.0.0']

setup_kwargs = {
    'name': 'peepshow',
    'version': '0.2.3',
    'description': 'Python data explorer.',
    'long_description': '# peepshow\n\nProvides following utilities for debugging Python applications:\n\n* show - lightweight function that prints name and value of your variable(s) to the console.\n* peep - featured, interactive interface for data inspection.\n\n![](https://user-images.githubusercontent.com/11185582/51219128-b3127780-192f-11e9-8618-ecfff642b87f.gif)\n\n## Resources\n\n* Documentation: <https://gergelyk.github.io/peepshow>\n* Repository: <https://github.com/gergelyk/peepshow>\n* Package: <https://pypi.python.org/pypi/peepshow>\n* Author: [Grzegorz Krasoń](mailto:grzegorz.krason@gmail.com)\n* License: [MIT](LICENSE)\n\n## Installation\n\nInstall `peepshow` package:\n\n```sh\npip install peepshow\n```\n\nPeepShow uses `clear`, `vim`, `man` commands which are available in most of Linux distributions. Users of other operating systems need to install them on their own.\n\n### Built-Ins\n\nIf you expect to use peepshow often, consider adding `peep` and `show` commands to Python\'s built-ins and enabling except hook. Edit either `{site-packages}/sitecustomize.py` or `{user-site-packages}/usercustomize.py` and append the following:\n\n```python\nimport peepshow\nimport builtins\nbuiltins.peep = peepshow.peep\nbuiltins.show = peepshow.show\nbuiltins.peep_ = peepshow.peep_\nbuiltins.show_ = peepshow.show_\npeepshow.enable_except_hook(consider_env=True)\n```\n\n### Breakpoint\n\nIt is also possible to invoke `peep()` as a result of calling built-in function `breakpoint()`. To enable such behavior use `PYTHONBREAKPOINT` system variable:\n\n```sh\nexport PYTHONBREAKPOINT=peepshow.peep\n```\n\n## Compatibility\n\n* This software is expected to work with Python 3.6, 3.7, 3.8 and compatible.\n* It has never been tested under operating systems other than Linux.\n* It works fine when started in a plain Python script, in ipython or ptipython.\n* In these environments like interactive python console, in pdb and ipdb, peep and show cannot infer names of the variables in the user context, so they need to be provided explicitly (e.g. use `peep_` and `show_`).\n\n## Usage\n\n### `show`\n\nRunning this script:\n\n```python\nx = 123\ny = {\'name\': \'John\', \'age\': 123}\nz = "Hello World!"\n\n# show all the variables in the scope\nshow()\n\n# or only variables of your choice\nshow(x, y)\n\n# you can also rename them\nshow(my_var=x)\n\n# use \'show_\' to specify variable names as a string\nshow_(\'x\')\n\n# expressions and renaming are also allowed\nshow_(\'x + 321\', zet=\'z\')\n```\n\nwill result in following output:\n\n```\nx = 123\ny = {\'age\': 123, \'name\': \'John\'}\nz = \'Hello World!\'\nx = 123\ny = {\'age\': 123, \'name\': \'John\'}\nmy_var = 123\nx = 123\nx + 321 = 444\nzet = \'Hello World!\'\n```\n\n### `peep`\n\nTry running the following script:\n\n```python\nx = 123\ny = {\'name\': \'John\', \'age\': 123}\nz = "Hello World!"\n\n# inspect dictionary that consists of all the variables in the scope\npeep()\n\n# or inspect variable of your choice directly\npeep(x)\n\n# use \'peep_\' to specify variable name as a string\npeep_(\'x\')\n```\n\nWhen interactive interface pops up:\n\n* Hit ENTER to see list of available variables.\n* Type `10` and hit ENTER to select `y`.\n* Hit ENTER again to see items of your dictionary.\n* Type `dir` and hit ENTER to list attributes of `y` (excluding built-ins).\n* Type `continue` and hit ENTER to proceed or type `quit` and hit ENTER to terminate your script.\n\nNote that all the commands have their short aliases. E.g. `quit` and `q` is the same.\n\nFor more help:\n\n* Type `help` and hit ENTER to see list of available commands.\n* Type `man` and hit ENTER to read the manual, hit `q` when you are done.\n\n### excepthook\n\nBefore running your script, set environment variable `PYTHON_PEEP_EXCEPTIONS` to `1`. Now run the script and see what happens when an exception is raised.\n\n## Development\n\n```sh\n# Preparing environment\npip install --user poetry  # unless already installed\npoetry install\n\n# Auto-formatting\npoetry run docformatter -ri peepshow tests\npoetry run isort -rc peepshow tests\npoetry run yapf -r -i peepshow tests\n\n# Checking coding style\npoetry run flake8 peepshow tests\n\n# Checking composition and quality\npoetry run vulture peepshow tests\npoetry run mypy peepshow tests\npoetry run pylint peepshow tests\npoetry run bandit peepshow tests\npoetry run radon cc peepshow tests\npoetry run radon mi peepshow tests\n\n# Testing with coverage\npoetry run pytest --cov peepshow --cov tests\n\n# Rendering documentation\npoetry run mkdocs serve\n\n# Building package\npoetry build\n\n# Releasing\npoetry version minor  # increment selected component\ngit commit -am "bump version"\ngit push\ngit tag ${$(poetry version)[2]}\ngit push --tags\npoetry build\npoetry publish\npoetry run mkdocs build\npoetry run mkdocs gh-deploy -b gh-pages\n```\n\n## Donations\n\nIf you find this software useful and you would like to repay author\'s efforts you are welcome to use following button:\n\n[![Donate](https://www.paypalobjects.com/en_US/PL/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=D9KUJD9LTKJY8&source=url)\n\n',
    'author': 'Grzegorz Krasoń',
    'author_email': 'grzegorz.krason@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gergelyk.github.io/peepshow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

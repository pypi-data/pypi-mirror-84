# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['topalias']

package_data = \
{'': ['*'], 'topalias': ['data/*']}

install_requires = \
['Click>=7.1,<8.0']

setup_kwargs = {
    'name': 'topalias',
    'version': '1.2.2',
    'description': 'Linux bash alias generator',
    'long_description': '# topalias\n\n[![Build Status](https://travis-ci.com/CSRedRat/topalias.svg?branch=master)](https://travis-ci.com/CSRedRat/topalias)\n[![Coverage](https://coveralls.io/repos/github/CSRedRat/topalias/badge.svg?branch=master)](https://coveralls.io/github/CSRedRat/topalias?branch=master)\n[![GitLab pipeline](https://gitlab.com/CSRedRat/topalias/badges/master/pipeline.svg)](https://gitlab.com/CSRedRat/topalias/-/pipelines)\n[![Python Version](https://img.shields.io/pypi/pyversions/topalias.svg)](https://pypi.org/project/topalias/)\n\n[topalias](https://github.com/CSRedRat/topalias) - Linux bash/zsh alias generator and statistics from command history, written on [Python](https://pypi.org/project/topalias/).\n\n## Features\n\n-   Generate short alias for popular command from bash history\n-   Fully typed with annotations and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)\n\n## Installation\n\nFrom [pypi.org repository](https://pypi.org/project/topalias/):\n\n```bash\npip3 install -U --user topalias\n```\n\nFrom source:\n\n```bash\ngit clone https://github.com/CSRedRat/topalias\npython3 topalias/setup.py install\n```\n\nRun as python script without install:\n\n```bash\ngit clone https://github.com/CSRedRat/topalias\npython3 topalias/topalias/cli.py -h\n```\n\n### Install requirements\n\n```bash\nsudo apt install python3 python3-pip -y\n```\n\n## Usage\n\n![generated bash aliases](images/bash_screenshot.png "Bash topalias output")\n\nShowcase how your project can be used:\n\n```bash\ntopalias # check if you uses aliases in ~/.bash_aliases - analyze and print usage statistics, offers to find new simple aliases\ntopalias -h # print help\ntopalias history # analyze local bash history\ntopalias h --acr=2 # set minimal length for generated acronym filter, so that exclude some short command and find long, hard, usable command\n```\n\nFile path search order:\n\n-   .bash_history in current . directory\n-   .bash_history in home ~ directory\n-   example development files in topalias/data\n\nRun as python module:\n\n```bash\npython3 -m topalias\n```\n\nAlso you can use topalias utility in [Bash for Git](https://gitforwindows.org/) on Windows and in [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux).\n\n## TODO\n\n-   zsh support\n-   exclude used alias from command chart\n-   alias use statistic\n-   only util in command without parameters usage statistic\n-   history file path parameter\n-   top command count parameter\n-   alias max length parameter\n-   snap package\n-   flatpak package\n\nPlease add you feature requests: [https://github.com/CSRedRat/topalias/issues/new](https://github.com/CSRedRat/topalias/issues/new)\n\n## License\n\n[GPLv3](https://github.com/CSRedRat/topalias/blob/master/LICENSE)\n\n## Contributors ✨\n\nThanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):\n\n<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->\n<!-- prettier-ignore-start -->\n<!-- markdownlint-disable -->\n<table>\n  <tr>\n    <td align="center"><a href="https://metin2wiki.ru/"><img src="https://avatars1.githubusercontent.com/u/1287586?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sergey Chudakov</b></sub></a><br /><a href="https://github.com/CSRedRat/topalias/commits?author=CSRedRat" title="Code">💻</a> <a href="#infra-CSRedRat" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="#ideas-CSRedRat" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-CSRedRat" title="Maintenance">🚧</a> <a href="#platform-CSRedRat" title="Packaging/porting to new platform">📦</a> <a href="#mentoring-CSRedRat" title="Mentoring">🧑\u200d🏫</a> <a href="#example-CSRedRat" title="Examples">💡</a></td>\n  </tr>\n</table>\n\n<!-- markdownlint-restore -->\n<!-- prettier-ignore-end -->\n\n<!-- ALL-CONTRIBUTORS-LIST:END -->\n\n_GitLab repository mirror with CI/CD: [https://gitlab.com/CSRedRat/topalias](https://gitlab.com/CSRedRat/topalias)_\n_GitHub Pages: [https://csredrat.github.io/topalias/](https://csredrat.github.io/topalias/)_\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CSRedRat/topalias',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['peerfeedback']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.1.3,<2.0.0', 'xlrd>=1.2.0,<2.0.0', 'xlsxwriter>=1.3.7,<2.0.0']

entry_points = \
{'console_scripts': ['peerfeedback = peerfeedback:run']}

setup_kwargs = {
    'name': 'peerfeedback',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Peer Feedback\n\n`peerfeedback` is a tool that creates pairings for people that give each other feedback. It makes sure that a person is not receiving feedback from a recipient of their own feedback to reduce the likelyhood of biased feedback.\n\n\n## Requirements\n\n1. Persons to match are identified by their email address\n1. Every email address is mapped to two other addresses, twice (once for receiving and once more for providing feedback)\n1. Email addresses shall not be matched mutually (if person `A` gives feedback to persons `B` and `C`, then persons `B` and `C` are not allowd to provide feedback to `A`) \n1. Input is done via a MS Office Excel sheet\n1. Output is done via a separate MS Office Excel sheet\n   1. Output format (each row in sheet): `(student)(reciver1)(reciver2)(giver1)(giver2)`\n   1. Automatically sent emails\n\n\n## Algorithm Used\n\nGiven persons `A`, `B`, `C`, `D`, `E`, the following pairing will be created. The person that provides feedback is listed on the lefthand side and the feedback targets on the righthand side.\n\n``` text\n`A` → `B`, `C`\n`B` → `C`, `D`\n`C` → `D`, `E`\n`D` → `E`, `A`\n`E` → `A`, `B`\n```\n\nWhich can be expressed by this general formula:\n\n``` text\nn(0)..n(max-2) → n+1, n+2\nn(max-1)       → n(max), n(0)\nn(max)         → n(0), n(1)\n```\n\n# License\n\nThis program was written by Alexander Graul <mail@agraul.de> and is licensed under the GNU General Public License version, either version 3 or (at your option) any later version.\n',
    'author': 'Alexander Graul',
    'author_email': 'mail@agraul.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mt103']
setup_kwargs = {
    'name': 'mt103',
    'version': '1.1.1',
    'description': 'Parse MT103 messages from the Swift payments network',
    'long_description': 'mt103\n=====\n\nParse MT103 messages from the Swift payments network\n\nWhat\'s an MT103?\n----------------\n\nBanks don\'t really deal with cash much any more.  Instead, they push bits\naround the internet tracking where your money goes digitally.  The network that\nhandles much of that movement is called `Swift`_, and the transfers are\ndocumented in a special format native to that network called *MT103*.\n\n.. _Swift: https://en.wikipedia.org/wiki/ISO_9362\n\n\nWhat\'s this Do?\n---------------\n\nUnfortunately, MT103 isn\'t a common standard for most software developers.\nIt\'s ugly & hard to read for humans and not at all easy to parse.  This library\nattempts to fix that, so all you have to do is pass an MT103 string into it and\nyou get back a native Python object with the properties you\'re looking for.\n\n.. code-block:: python\n\n    from mt103 import MT103\n\n    mt103 = MT103("some-mt-103-string")\n    print("basic header: {}, bank op code: {}, complete message: {}".format(\n        mt103.basic_header,\n        mt103.text.bank_operation_code,\n        mt103\n    ))\n\n\nInstallation\n------------\n\nIt\'s on PyPi, so just install it with pip.\n\n.. code-block:: shell\n\n    $ pip install mt103\n\n\nTODO\n----\n\nParsing MT103 messages should work just fine and you should be able to access\nall of the components via the Python API *except* for section ``13C``.  From\nthe specs I\'ve seen, it\'s unclear as to whether this section is permitted to\nrepeat (meaning it should be parsed as a list) or if it\'s one value only.  If\nsomeone can explain this authoritatively to me, I can include support for this\nsection as well.',
    'author': 'Daniel Quinn',
    'author_email': 'code@danielquinn.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danielquinn/mt103',
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

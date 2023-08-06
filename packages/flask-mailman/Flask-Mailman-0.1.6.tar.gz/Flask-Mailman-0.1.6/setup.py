# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_mailman', 'flask_mailman.backends']

package_data = \
{'': ['*']}

install_requires = \
['flask>=1.0,<2.0']

setup_kwargs = {
    'name': 'flask-mailman',
    'version': '0.1.6',
    'description': "Porting Django's email implementation to your Flask applications.",
    'long_description': "# Flask-Mailman\n\nFlask-Mailman is a Flask extension providing simple email sending capabilities.\n\nIt was meant to replace unmaintained Flask-Mail with a better warranty and more features.\n\n## Usage\n\nFlask-Mail ported Django's email implementation to your Flask applications, which may be the best mail sending implementation that's available for python.\n\nThe way of using this extension is almost the same as Flask-Mail and also Django.\n\nYou can just read their documentation and choose a preferred style.\n\nDjango documentation: https://docs.djangoproject.com/en/2.2/topics/email/\n\nFlask-Mail documentation: http://packages.python.org/Flask-Mail",
    'author': 'Waynerv',
    'author_email': 'ampedee@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/waynerv/flask-mailman',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

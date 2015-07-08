try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'craigslister app',
    'author': 'Michael Burt',
    'url': 'http://mpburt.com/craigslister/',
    'download_url': 'http://mpburt.com/craigslister/craigslister.zip',
    'author_email': 'micahelpburt@gmail.com',
    'version': '0.1',
    'install_requires': ['sqlalchemy','MySQLdb','requests','datetime','time','pandas','twython'],
    'packages': ['CRAIGSLISTER'],
    'scripts': ['bin/craigslister_.py','bin/craigslister_.sh','bin/schema.sql'],
    'name': 'craigslister'
}

setup(**config)
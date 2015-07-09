import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
  long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
except:
  long_description = u"Python package for Quandl API access"

setup(
    name = 'craigslister',
    description = 'craigslister app',
    long_description = long_description
    version = '0.1'
    author = 'Michael Burt',
    url = 'http://mpburt.com/craigslister/',
    download_url = 'http://mpburt.com/craigslister/craigslister.tar.gz'
    install_requires = ['sqlalchemy','MySQLdb','requests','datetime','time','pandas','twython'],
    packages = ['Craigslister'],
    scripts = ['bin/craigslister_.py'],
)

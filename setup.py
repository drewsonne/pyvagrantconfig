from setuptools import setup, find_packages
import sys

PY_VERSION = sys.version_info[:2]
PY2 = (PY_VERSION[0] == 2)
PY3 = (PY_VERSION[0] == 3)

requirements = [ ]

if sys.version_info[:2] == (2, 6):
    requirements.append('ordereddict')


setup(
    name='pyvagrantconfig',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=requirements,
    author_email='drew.sonne@gmail.com',
    author='Drew J. Sonne',
    url='https://github.com/drewsonne/pyvagrant-config'
)

from setuptools import setup, find_packages

setup(
    name='pyvagrantconfig',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'pypeg2'
    ],
    author_email='drew.sonne@gmail.com',
    author='Drew J. Sonne',
    url='https://github.com/drewsonne/pyvagrant-config'
)

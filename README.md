# pyvagrantconfig
Write a description of what your utility does

## Setup
If there are any requirements for getting started (non-pip dependencies, external systems, etc.) add those here

## Deployment
When this is ready to be deployed, you can upload it to the nordcloud pip server

    $ cd $WORKSPACE/pyvagrantconfig
    $ python setup.py sdist upload

## Installation
After it's on the nordcloud pip server, you should be able to install on the client by running

    $ pip install pyvagrantconfig

## Usage

## Contributing
If someone were to modify this utility, is there anything important about it that they should know?
### virtualenv
When doing development and testing, it's good practice to use a virtualenv. A virtualenv is a sandboxed python environment which does not modify the system python installation
You can install one as follows:

    $ pip install virtualenv
    $ cd $WORKSPACE/pyvagrantconfig
    $ virtualenv venv
    $ . ./venv/bin/activate
    (pyvagrantconfig)$

Now that you have a working virtualenv, you can install the utility in development mode. Keep in mind that the 'activate' step, is valid only for a single session. If you close the terminal
you'll have to run `venv/bin/activate` again. You can now run pip, python, and pyvagrantconfig while only referring to the local python environment created in $WORKSPACE/pyvagrantconfig. You can see this by running:

    (pyvagrantconfig)$ which pip
    $WORKSPACE/pyvagrantconfig/venv/bin/python
    (pyvagrantconfig)$ which python

### Development Mode
When testing this utility, you can install it and still edit the source files as follows:

    $ cd $WORKSPACE/pyvagrantconfig
    $ pip install --editable .


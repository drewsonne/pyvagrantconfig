[![Build Status](https://travis-ci.org/drewsonne/pyvagrantfile.svg?branch=master)](https://travis-ci.org/drewsonne/pyvagrantfile)

# pyvagrantfile
Parses a vagrant file into a python object for inspect. Mainly used to read and build Vagrant file in python.
I built this to help me write a utility in python which can build projects and convert Vagrantfiles to packer files.

## Supported Directives

 - Most vm.config directives,
 - Chef provisioner
 - Shell provisioner
 - VB provider

## Installation
After it's on the pip server, you should be able to install on the client by running

    $ pip install pyvagrantfile

## Deployment
When this is ready to be deployed, you can upload it to the pip server

    $ cd $WORKSPACE/pyvagrantfile
    $ python setup.py sdist upload


## Usage

## Contributing

### virtualenv
When doing development and testing, it's good practice to use a virtualenv. A virtualenv is a sandboxed python environment which does not modify the system python installation
You can install one as follows:

    $ pip install virtualenv
    $ cd $WORKSPACE/pyvagrantfile
    $ virtualenv venv
    $ . ./venv/bin/activate
    (pyvagrantfile)$

Now that you have a working virtualenv, you can install the utility in development mode. Keep in mind that the 'activate' step, is valid only for a single session. If you close the terminal
you'll have to run `venv/bin/activate` again. You can now run pip, python, and pyvagrantfile while only referring to the local python environment created in $WORKSPACE/pyvagrantfile. You can see this by running:

    (pyvagrantfile)$ which pip
    $WORKSPACE/pyvagrantfile/venv/bin/python
    (pyvagrantfile)$ which python

### Development Mode
When testing this utility, you can install it and still edit the source files as follows:

    $ cd $WORKSPACE/pyvagrantfile
    $ pip install --editable .

### Roadmap
I intially tried to use pyPEG, but could not get a handle on it, so for now, we use a custom state parser.
I want to move this to a PEG parser to make it easier to manage, but in the spirit of minimum viable product, it's up and out.

 - This is currently way too specific. Needs to be rewritten to parse general ruby structures and extract details out of it, rather than looking for particular vagrant configurations.
 - Port parser from state parser to PEG parser.
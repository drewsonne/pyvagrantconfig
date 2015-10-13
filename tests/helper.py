import os
from pyvagrantconfig import PY_VERSION

__author__ = 'drews'


def get_test_root():
    """
    Get the test directory root path
    :return: Path to the root of the test directory
    """
    return os.path.dirname(os.path.realpath(__file__))

def get_vagrant_file_path(name):
    """
    Get the path to a vagrant file in test resources.
    :param name:
    :return:
    """
    if PY_VERSION == (2,6):
        format = "{0}/resources/vagrant-files/{1}"
    else:
        format = "{}/resources/vagrant-files/{}"
    return (format).format(get_test_root(), name)

def load_vagrant_file(name):
    """
    Get the vagrant file from test resources.
    :param name:
    :return:
    """
    with open(get_vagrant_file_path(name), 'r') as vagrantfile:
        return vagrantfile.read()
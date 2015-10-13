from tests.TestVagrantCase import TestVagrantCase
from tests.helper import load_vagrant_file, get_vagrant_file_path
from pyvagrantconfig.Parser import VagrantParser
from pyvagrantconfig import Vagrantfile

__author__ = 'drews'


class TestPyVagrantfile(TestVagrantCase):

    def test_chef_provisioner(self):
        vagrantfile_string = load_vagrant_file('default-chef')
        vagrantfile = VagrantParser.parses(content=vagrantfile_string)

        provisioner = vagrantfile.vm.provision

        self.assertKeyInDict('chef_solo', provisioner)
        chef_solo = provisioner['chef_solo']

        self.assertHasAttr(chef_solo, 'cookbooks_path')
        self.assertListEqual(chef_solo.cookbooks_path, ['cookbooks','my_cookbooks'])

        self.assertHasAttr(chef_solo, 'data_bags_path')
        self.assertEqual(chef_solo.data_bags_path, 'data_bags')

        self.assertHasAttr(chef_solo, 'roles_path')
        self.assertEqual(chef_solo.roles_path, 'roles')

        self.assertHasAttr(chef_solo, 'roles')
        self.assertListEqual(chef_solo.roles, ['web','database'])

        self.assertHasAttr(chef_solo, 'cookbooks_path')
        self.assertListEqual(chef_solo.cookbooks_path, ['cookbooks', 'my_cookbooks'])

        self.assertHasAttr(chef_solo, 'json')
        self.assertDictEqual(chef_solo.json, {
            'apache' : {
                'listen_address' : '0.0.0.0',
                'modules': ['mod_sec', 'mod_php', 'mod_cgi', 'mod_java']
            }
        })

        self.assertHasAttr(chef_solo, 'recipes')
        self.assertListEqual(chef_solo.recipes, ['apache', 'mysql'])




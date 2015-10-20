from __future__ import unicode_literals
from tests.TestVagrantCase import TestVagrantCase
from tests.helper import load_vagrant_file
from pyvagrantfile.Parser import VagrantParser

__author__ = 'drews'


class TestPyVagrantfile(TestVagrantCase):
    def test_to_dict(self):
        vagrantfile_string = load_vagrant_file('default-chef')
        vagrantfile = VagrantParser.parses(content=vagrantfile_string)

        self.assertDictEqual(vagrantfile.to_dict(), {
            'vm': {
                'box': 'base',
                'box_check_update': False,
                'provision': {
                    'shell': {
                        'inline': 'sudo apt-get update\nsudo apt-get install -y apache2'
                    },
                    'chef_solo': {
                        'data_bags_path': 'data_bags',
                        'roles_path': 'roles',
                        'roles': ['web', 'database'],
                        'recipes': ['apache', 'mysql'],
                        'cookbooks_path': ['cookbooks', 'my_cookbooks'],
                        'json': {
                            'apache': {
                                'listen_address': '0.0.0.0',
                                'modules': ['mod_sec', 'mod_php', 'mod_cgi', 'mod_java']
                            }
                        }
                    }
                },
                'network': {
                    'forwarded_port': [{
                        'host': 8080,
                        'guest': 80
                    }],
                    'private_network': {
                        'ip': '192.168.33.10'
                    },
                    'public_network': True
                },
                'provider': {
                    'virtualbox': {
                        'gui': True,
                        'memory': '1024'
                    }
                }
            }
        })

    def test_chef_provisioner(self):
        vagrantfile_string = load_vagrant_file('default-chef')
        vagrantfile = VagrantParser.parses(content=vagrantfile_string)

        provisioner = vagrantfile.vm.provision

        self.assertKeyInDict('chef_solo', provisioner)
        chef_solo = provisioner['chef_solo']

        self.assertHasAttr(chef_solo, 'cookbooks_path')
        self.assertListEqual(chef_solo.cookbooks_path, ['cookbooks', 'my_cookbooks'])

        self.assertHasAttr(chef_solo, 'data_bags_path')
        self.assertEqual(chef_solo.data_bags_path, 'data_bags')

        self.assertHasAttr(chef_solo, 'roles_path')
        self.assertEqual(chef_solo.roles_path, 'roles')

        self.assertHasAttr(chef_solo, 'roles')
        self.assertListEqual(chef_solo.roles, ['web', 'database'])

        self.assertHasAttr(chef_solo, 'cookbooks_path')
        self.assertListEqual(chef_solo.cookbooks_path, ['cookbooks', 'my_cookbooks'])

        self.assertHasAttr(chef_solo, 'json')
        self.assertDictEqual(chef_solo.json, {
            'apache': {
                'listen_address': '0.0.0.0',
                'modules': ['mod_sec', 'mod_php', 'mod_cgi', 'mod_java']
            }
        })

        self.assertHasAttr(chef_solo, 'recipes')
        self.assertListEqual(chef_solo.recipes, ['apache', 'mysql'])

    def test_chef_provisioner2(self):
        vagrantfile_string = load_vagrant_file('default-chef2')
        vagrantfile = VagrantParser.parses(content=vagrantfile_string)

        provisioner = vagrantfile.vm.provision

        self.assertKeyInDict('chef_solo', provisioner)
        chef_solo = provisioner['chef_solo']

        self.assertHasAttr(chef_solo, 'cookbooks_path')
        self.assertListEqual(chef_solo.cookbooks_path, ['cookbooks', 'site-cookbooks'])

        self.assertHasAttr(chef_solo, 'json')
        self.assertDictEqual(chef_solo.json, {
            'ncpackageserver': {
                'nginx_port': 8080,
                'authentication': {
                    'htpasswd': 'auth/htpasswd_devpi',
                    'users': [{
                        'name': 'drewsonne',
                        'password': 'password'
                    }]
                }
            }
        })

        self.assertHasAttr(chef_solo, 'run_list')
        self.assertListEqual(chef_solo.run_list, [
            'recipe[devpi::server]',
            'recipe[ncpackageserver::web]',
            'recipe[ncpackageserver::nginx]',
            'recipe[ncpackageserver::server]'
        ])

from tests.TestVagrantCase import TestVagrantCase
from tests.helper import load_vagrant_file, get_vagrant_file_path
from pyvagrantconfig.Parser import VagrantParser
from pyvagrantconfig import Vagrantfile

__author__ = 'drews'


class TestPyVagrantfile(TestVagrantCase):
    def test___init___(self):
        vagrantfile_string = load_vagrant_file('default')
        vagrantfile = VagrantParser.parses(content=vagrantfile_string)
        self.assertIsInstance(vagrantfile, Vagrantfile)

        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = VagrantParser.parsep(path=vagrantfile_path)
        self.assertIsInstance(vagrantfile, Vagrantfile)

        self.assertEqual(vagrantfile.configure_version, '2')

    def test_vm_attributes(self):
        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = VagrantParser.parsep(path=vagrantfile_path)

        self.assertHasAttr(vagrantfile, 'vm')
        vm = vagrantfile.vm

        self.assertHasAttr(vm, 'box')
        self.assertEqual(vm.box, 'base')

        self.assertHasAttr(vm, 'box_check_update')
        self.assertEqual(vm.box_check_update, False)

    def test_network_attributes(self):
        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = VagrantParser.parsep(path=vagrantfile_path)

        self.assertHasAttr(vagrantfile.vm, 'network')
        network = vagrantfile.vm.network

        self.assertKeyInDict('forwarded_port', network)
        self.assertIsInstance(network['forwarded_port'], list)
        self.assertGreater(len(network['forwarded_port']), 0)

        self.assertHasAttr(network['forwarded_port'][0], 'guest')
        self.assertEqual(network['forwarded_port'][0].guest, 80)

        self.assertHasAttr(network['forwarded_port'][0], 'host')
        self.assertEqual(network['forwarded_port'][0].host, 8080)

        self.assertKeyInDict('private_network', network)

        self.assertHasAttr(network['private_network'], 'ip')
        self.assertEqual(network['private_network'].ip, '192.168.33.10')

        self.assertKeyInDict('public_network', network)
        self.assertTrue(network['public_network'])

    def test_synced_folder(self):
        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = VagrantParser.parsep(path=vagrantfile_path)

        self.assertHasAttr(vagrantfile.vm, 'synced_folder')
        self.assertTupleEqual(vagrantfile.vm.synced_folder, ('../data', '/vagrant_data'))

    def test_provider_virtualbox(self):
        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = VagrantParser.parsep(path=vagrantfile_path)

        self.assertHasAttr(vagrantfile.vm, 'provider')
        self.assertKeyInDict('virtualbox', vagrantfile.vm.provider)
        vb = vagrantfile.vm.provider['virtualbox']

        self.assertHasAttr(vb, 'gui')
        self.assertTrue(vb.gui, True)

        self.assertHasAttr(vb, 'memory')
        self.assertTrue(vb.memory, '1024')

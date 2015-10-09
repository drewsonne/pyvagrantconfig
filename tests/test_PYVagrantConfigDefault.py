from tests.TestVagrantCase import TestVagrantCase
from tests.helper import load_vagrant_file, get_vagrant_file_path
from pyvagrantconfig.Parser import Parser
from pyvagrantconfig import Vagrantfile

__author__ = 'drews'

class TestPyVagrantfile(TestVagrantCase):

    def test___init___(self):
        vagrantfile_string = load_vagrant_file('default')
        vagrantfile = Parser.parses(content=vagrantfile_string)
        self.assertIsInstance(vagrantfile, Vagrantfile)

        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = Parser.parsep(path=vagrantfile_path)
        self.assertIsInstance(vagrantfile, Vagrantfile)

        self.assertEqual(vagrantfile.configure_version, 2)

    def test_vm_attributes(self):
        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = Parser.parse(path=vagrantfile_path)

        self.assertHasAttr(vagrantfile, 'vm')
        vm = vagrantfile.vm

        self.assertHasAttr(vm, 'box')
        self.assertEqual(vm.box, 'base')

        self.assertHasAttr(vm, 'box_check_update')
        self.assertEqual(vm.box_check_update, False)


    def test_network_attributes(self):
        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = Parser.parse(path=vagrantfile_path)

        self.assertHasAttr(vagrantfile.vm, 'network')
        network = vagrantfile.vm.network

        self.assertKeyInDict(network, 'forwarded_port')

        self.assertHasAttr(network['forwarded_port'], 'guest')
        self.assertEqual(network['forwarded_port'].guest, 80)

        self.assertHasAttr(network['forwarded_port'], 'host')
        self.assertEqual(network['forwarded_port'].host, 8080)

        self.assertKeyInDict(network, 'private_network')

        self.assertHasAttr(network['private_network'], 'ip')
        self.assertEqual(network['private_network'].ip, '192.168.33.10')

        self.assertKeyInDict(network, 'public_network')

    def test_synced_folder(self):
        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = Parser.parse(path=vagrantfile_path)

        self.assertKeyInDict(vagrantfile.vm, 'synced_folder')
        self.assertDictEqual(vagrantfile.vm.synced_folder, ['../data', '/vagrant_data'])

    def test_provider_virtualbox(self):
        vagrantfile_path = get_vagrant_file_path('default')
        vagrantfile = Parser.parse(path=vagrantfile_path)

        self.assertHasAttr(vagrantfile.vm, 'provider')
        self.assertKeyInDict('virtualbox', vagrantfile.vm.provider)
        vb = vagrantfile.vm.provider['virtualbox']

        self.assertHasAttr(vb, 'gui')
        self.assertTrue(vb.gui, True)

        self.assertHasAttr(vb, 'memory')
        self.assertTrue(vb.memory, '1024')
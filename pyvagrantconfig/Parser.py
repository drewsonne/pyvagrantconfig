from pypeg2 import *
from pyvagrantconfig import Vagrantfile, VagrantfileVm, VagrantfileProviderVb, VagrantfileNetworkForwardedPort, \
    VagrantfileNetworkPrivateNetwork, VagrantfileProvisionShell

__author__ = 'drews'


class VagrantParser(object):
    STATE_SEARCHING_FOR_HEADING = 0
    STATE_LOOKING_FOR_CONFIG = 1
    PARSING_VM_CONFIG = 2
    PARSING_NETWORK = 3
    PARSING_SYNCED_FOLDER = 4
    PARSING_PROVIDER = 5
    PARSING_PROVIDER_VB = 6
    PARSING_PROVISIONER = 7
    PARSING_PROVISIONER_SHELL = 8

    @classmethod
    def parses(cls, content):
        return cls(content).parse()

    @classmethod
    def parsep(cls, path):
        with open(path, 'r') as vagrantfile:
            return cls.parses(vagrantfile.read())

    def __init__(self, content):
        self.vagrantfile = content

    def parse(self):
        # parsed = parse(
        #     self.vagrantfile,
        #     VagrantGrammar,
        #     comment=comment_sh
        # )

        vagrantfile = Vagrantfile()

        self.current_position = 0
        self.current_state = self.STATE_SEARCHING_FOR_HEADING
        while self.current_position < len(self.vagrantfile):
            self.strip_indent()
            if self.is_comment_line():
                self.progress_to_eol()
                continue

            if self.current_state == self.STATE_SEARCHING_FOR_HEADING:
                configure_intro = 'Vagrant.configure('
                if self.parse_text().startswith(configure_intro):
                    self.current_state = self.STATE_LOOKING_FOR_CONFIG
                    self.progress_parser(configure_intro)
                    setattr(vagrantfile, 'configure_version', self.parse_text()[0])
                    self.progress_parser(1)
                    matches = re.match(r'([^\n]+)', self.parse_text()).groups()
                    self.progress_parser(matches[0])
            elif self.current_state == self.STATE_LOOKING_FOR_CONFIG:
                if self.parse_text().startswith('config.'):
                    self.progress_parser('config.')
                    config_type_matches = re.match(r'[^\.]+', self.parse_text())
                    if config_type_matches is not None:
                        config_type = config_type_matches.group(0)
                        if config_type == 'vm':
                            self.current_state = self.PARSING_VM_CONFIG
                elif self.parse_text().startswith('end'):
                    self.progress_to_eol()
            elif self.current_state == self.PARSING_VM_CONFIG:
                vm_config_type = re.match(r'vm.([^\.\s]+)', self.parse_text())
                if vm_config_type is not None:
                    vm_config_type = vm_config_type.group(1)
                    if vm_config_type in ['network']:
                        self.current_state = self.PARSING_NETWORK
                    elif vm_config_type == 'synced_folder':
                        self.current_state = self.PARSING_SYNCED_FOLDER
                    elif vm_config_type == 'provider':
                        self.current_state = self.PARSING_PROVIDER
                    elif vm_config_type == 'provision':
                        self.current_state = self.PARSING_PROVISIONER
                    else:
                        vm_config_matches = re.match(r'vm.([^\s]+)\s?=\s?([^\n]+)', self.parse_text())
                        if vm_config_matches is not None:
                            if hasattr(vagrantfile, 'vm'):
                                vm_config = vagrantfile.vm
                            else:
                                vm_config = VagrantfileVm()

                            config_match = vm_config_matches.groups()
                            key = config_match[0]
                            value = config_match[1]
                            if value[0] in ["'", '"']:
                                value = value[1:len(value) - 1]
                            elif value in ['true', 'false']:
                                value = (value == 'true')
                            elif re.match(r'\d+', value):
                                value = int(value)
                            setattr(vm_config, key, value)
                            setattr(vagrantfile, 'vm', vm_config)
                            self.progress_parser(re.match(r'[^\n]+', self.parse_text()).group(0))
                            self.current_state = self.STATE_LOOKING_FOR_CONFIG
                        elif self.parse_text().startswith('end'):
                            self.current_position = len(self.vagrantfile)

            elif self.current_state == self.PARSING_PROVISIONER:
                self.progress_parser('vm.provision "')
                provisioner_type = re.match(r'([^\'"]+)', self.parse_text()).group(0)
                if provisioner_type == 'shell':

                    if not hasattr(vagrantfile.vm, 'provision'):
                        setattr(vagrantfile.vm, 'provision', { provisioner_type: VagrantfileProvisionShell() })

                    self.current_state = self.PARSING_PROVISIONER_SHELL
                    self.progress_parser_to_char(' ')
                pass

            elif self.current_state == self.PARSING_PROVISIONER_SHELL:
                if self.parse_text().startswith('inline'):
                    self.progress_parser('inline: ')
                    if self.parse_text()[0:3] == '<<-':
                        shell_content = self.parse_provisioner_shell_inline()
                        setattr(vagrantfile.vm.provision['shell'], 'inline', shell_content)
                    else:
                        shell_content = self.parse_variable()
                    self.current_state = self.STATE_LOOKING_FOR_CONFIG
            elif self.current_state == self.PARSING_PROVIDER:
                self.progress_parser('vm.provider ')
                provider_type = re.match(r'[\'"]([^\'"]+)[\'"] do \|([^\|]+)\|', self.parse_text()).groups()
                self.provider_type = provider_type[0]
                self.provider_prefix = provider_type[1]
                self.current_state = self.PARSING_PROVIDER_VB
                self.progress_to_eol()
                if not hasattr(vagrantfile.vm, 'provider'):
                    setattr(vagrantfile.vm, 'provider', {self.provider_type: VagrantfileProviderVb()})



            elif self.current_state == self.PARSING_PROVIDER_VB:
                if self.parse_text().startswith('end'):
                    self.progress_to_eol()
                    self.current_state = self.STATE_LOOKING_FOR_CONFIG
                else:
                    vb_provider_config_option = re.match(r'{}.([^\s]+)\s?=\s?([^\n]+)'.format(self.provider_prefix),
                                                         self.parse_text()).groups()
                    setattr(vagrantfile.vm.provider[self.provider_type], vb_provider_config_option[0],
                            vb_provider_config_option[1])
                    self.progress_to_eol()

            elif self.current_state == self.PARSING_SYNCED_FOLDER:
                synced_folder_matches = re.match(r'vm.synced_folder\s+["\']([^\'"]+)["\'],\s+["\']([^\'"]+)["\']',
                                                 self.parse_text()).groups()
                setattr(vagrantfile.vm, 'synced_folder', synced_folder_matches)
                self.progress_to_eol()
                self.current_state = self.STATE_LOOKING_FOR_CONFIG

            elif self.current_state == self.PARSING_NETWORK:
                self.progress_parser('vm.network "')
                if not hasattr(vagrantfile.vm, 'network'):
                    network = {}
                else:
                    network = vagrantfile.vm.network

                if self.parse_text().startswith('forwarded_port'):
                    self.progress_parser(re.match(r'([^,]+)', self.parse_text()).group(1))
                    port_forwarding_matches = re.match(r',\s*guest:\s?(\d+),\s?host:\s(\d+)', self.parse_text())
                    port_forwarding_matches = port_forwarding_matches.groups()
                    forwarded_port = VagrantfileNetworkForwardedPort(port_forwarding_matches[0],
                                                                     port_forwarding_matches[1])
                    if 'forwarded_port' not in network:
                        network = {
                            'forwarded_port': [forwarded_port]
                        }
                    else:
                        network['forwarded_port'].append(forwarded_port)
                elif self.parse_text().startswith('private_network'):
                    self.progress_parser(re.match(r'([^,]+)', self.parse_text()).group(1))
                    private_network_forwarding_matches = re.match(r',\s*ip:\s?[\'"]([^\'"]+)[\'"]',
                                                                  self.parse_text()).groups()

                    private_network = VagrantfileNetworkPrivateNetwork(private_network_forwarding_matches[0])

                    network['private_network'] = private_network
                elif self.parse_text().startswith('public_network'):

                    network['public_network'] = True

                setattr(vagrantfile.vm, 'network', network)
                self.progress_to_eol()
                self.current_state = self.STATE_LOOKING_FOR_CONFIG
            else:
                self.progress_parser(1)

        return vagrantfile

    def progress_parser(self, progress_unit=1):
        if isinstance(progress_unit, int):
            self.current_position = self.current_position + progress_unit
        elif isinstance(progress_unit, str):
            self.current_position = self.current_position + len(progress_unit)
        else:
            raise Exception("Unexpected progress_unit '{}'".format(progress_unit))

    def parse_text(self):
        return self.vagrantfile[self.current_position:len(self.vagrantfile)]

    def strip_indent(self):
        matches = re.match(r'([\n\s]+)', self.parse_text())
        if matches is not None:
            self.progress_parser(matches.group(0))

    def is_comment_line(self):
        return self.parse_text().startswith('#')

    def progress_to_eol(self):
        matches = re.match('([^\n]*\n)', self.parse_text())
        if matches is not None:
            self.progress_parser(matches.group(0))
        else:
            self.progress_parser(
                len(self.parse_text()))  # If we have no carriage returns, we're at the end of the file.

    def progress_parser_to_char(self, char):
        if char in [',']:
            char = '\,'
        matches = re.match('([^{}]+)'.format(char), self.parse_text())
        if matches is not None:
            self.progress_parser(matches.group(0))

    def parse_provisioner_shell_inline(self):
        keep_parsing = True
        FIND_DELIMETER = 0
        READ_DELIMETER = 1
        LOOKING_FOR_CLOSING_DELIMITER = 2
        CHECKING_CLOSING_DELIMITER = 3
        state = FIND_DELIMETER
        delimiter = ''
        inline_script = ''
        closing_delimiter = ''
        while keep_parsing:
            char = self.parse_text()[0]
            if state == FIND_DELIMETER:
                if char == '-':
                    self.progress_parser()
                    state = READ_DELIMETER
                else:
                    self.progress_parser()
            elif state == READ_DELIMETER:
                if char != "\n":
                    delimiter += str(char)
                else:
                    state = LOOKING_FOR_CLOSING_DELIMITER
                self.progress_parser()
            elif state == LOOKING_FOR_CLOSING_DELIMITER:
                if char == delimiter[0]:
                    state = CHECKING_CLOSING_DELIMITER
                else:
                    inline_script += str(char)
                    self.progress_parser()
            elif state == CHECKING_CLOSING_DELIMITER:
                if char == delimiter[len(closing_delimiter)]:
                    closing_delimiter += str(char)
                    self.progress_parser()
                if closing_delimiter == delimiter:
                    keep_parsing = False
        self.progress_to_eol()
        # shell_content = re.match(r'([^>]+)', self.parse_text()).group(0)
        return inline_script

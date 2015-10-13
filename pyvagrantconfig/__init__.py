__author__ = 'drews'

class Vagrantfile(object):

    def __init__(self):
        self.struct = None

    def __getattr__(self, name):
        return getattr(self.struct, name)


class VagrantfileVm(object): pass

class VagrantfileProviderVb(object): pass

class VagrantfileProvisionShell(object): pass

class VagrantfileProvisionChef(object):
    def __init__(self):
        self.roles = []
        self.recipes = []

    def add_recipe(self, new_recipe):
        self.recipes.append(new_recipe)

    def add_role(self, new_role):
        self.roles.append(new_role)

class VagrantfileProvisionPuppet(object): pass

class VagrantfileNetworkForwardedPort(object):
    def __init__(self, guest, host):
        self.guest = int(guest)
        self.host = int(host)

class VagrantfileNetworkPrivateNetwork(object):
    def __init__(self, ip=None):
        self.ip = ip
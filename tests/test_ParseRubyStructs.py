from pyvagrantconfig.Parser import VagrantParser
from tests.TestVagrantCase import TestVagrantCase

__author__ = 'drews'


class TestPyVagrantfile(TestVagrantCase):
    def test_parse_ruby_dict(self):
        parser = VagrantParser(content='')
        parser.current_position = 0
        ruby_dict = parser.parse_ruby_dict("""
    {
      "apache" => {
        "listen_address" => "0.0.0.0",
        "modules" => ["mod_sec", "mod_php", "mod_cgi", "mod_java"]
      }
    }""")

        self.assertDictEqual(ruby_dict, {
            'apache': {
                'listen_address': '0.0.0.0',
                'modules': ['mod_sec', 'mod_php', 'mod_cgi', 'mod_java']
            }
        })

    def test_parse_ruby_dict_malformed(self):
        parser = VagrantParser(content='')
        parser.current_position = 0
        ruby_dict = parser.parse_ruby_dict("""
      "apache" => {
        "listen_address" => "0.0.0.0",
        "modules" => ["mod_sec", "mod_php", "mod_cgi", "mod_java"]
      }
    }""")

        self.assertDictEqual(ruby_dict, {
            'apache': {
                'listen_address': '0.0.0.0',
                'modules': ['mod_sec', 'mod_php', 'mod_cgi', 'mod_java']
            }
        })

    def test_parse_ruby_dict_extended(self):
        parser = VagrantParser(content='')
        parser.current_position = 0
        ruby_dict = parser.parse_ruby_dict("""
    {
      "apache" => {
        "listen_address" => "0.0.0.0",
        "modules" => ["mod_sec", "mod_php", "mod_cgi", "mod_java"]
      }
    }

    chef.add_recipe "apache"
    chef.add_recipe "mysql""")

        self.assertDictEqual(ruby_dict, {
            'apache': {
                'listen_address': '0.0.0.0',
                'modules': ['mod_sec', 'mod_php', 'mod_cgi', 'mod_java']
            }
        })

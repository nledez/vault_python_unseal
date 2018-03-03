'''
Unseal vault config management
'''

import os
import sys
import yaml

CONFIG_PATH = '~/.unseal_vault.yml'


def load():
    if not os.path.exists(CONFIG_PATH):
        print('Missing ~/.unseal_vault.yml file. Please create it.')
        sys.exit(1)
    else:
        with open(CONFIG_PATH, 'r') as stream:
            try:
                return yaml.load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(1)

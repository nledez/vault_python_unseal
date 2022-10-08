'''
Unseal vault servers trouth ssh tunnel
Get keys store in passwordstore as yaml
'''
import os
import yaml
import sys

from .op import get_config_op
from .op_legacy import get_config_op_legacy


def get_config(config_name, yaml_file='~/.unseal_vault.yml'):
    '''
    Get config wrapper

    *config_type* need to be defined as 'passtore' or 'yaml'

    *path* the pass to get yaml configuration
    '''

    full_path = os.path.expanduser(yaml_file)
    if not os.path.exists(full_path):
        print('Missing {} file. Please create it.'.format(full_path))
        sys.exit(1)
    else:
        with open(full_path, 'r') as stream:
            try:
                return yaml.load(stream, Loader=yaml.FullLoader)[config_name]
            except KeyError as k:
                print(f'Missing config: {k}')
                sys.exit(1)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(1)


def handle_config(config):
    if config['type'] == 'op':
        return get_config_op(config)
    if config['type'] == 'op_legacy':
        return get_config_op_legacy(config)

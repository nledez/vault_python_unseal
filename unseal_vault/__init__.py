'''
Unseal vault servers trouth ssh tunnel
Get keys store in passwordstore as yaml
'''
import subprocess
import consul
import hvac
import yaml
import sys


def get_config(config_type, path):
    '''
    Get config wrapper

    *config_type* need to be defined as 'passtore' or 'yaml'

    *path* the pass to get yaml configuration
    '''
    if config_type == 'passtore':
        return get_config_passtore(path)
    elif config_type == 'yaml':
        return get_config_yaml(path)


def get_config_passtore(pass_name):
    '''
    Get config in passwordstore and convert it as yaml

    *pass_name* is the name of documents contain config
    '''
    stream = subprocess.check_output('pass show {}'.format(pass_name),
                                     shell=True)
    try:
        return yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)


def get_config_yaml(yaml_file):
    '''
    Get config in yaml file to avoid password store stuff

    *yaml_file* is the filename contain config
    '''
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)


def consul_get_vault_server(vault_name):
    '''
    Get vault server list in Consul
    And keep only important fields

    *vault_name* is the Vault service name defined in Consul
    '''
    consul_client = consul.Consul()
    servers = list(map(
        lambda e: {
            'node_name': e['Node'],
            'address': e['ServiceAddress'],
            'port': e['ServicePort']
        },
        consul_client.catalog.service(vault_name)[1]
    ))
    return servers


def unseal(host, port, unseal_keys, name=None):
    '''
    Unseal one server

    *host* the hostname or ip server want to unlock

    *port* the Vault TCP port

    *unseal_keys* the unseal keys list
    '''
    if name:
        print('{}:'.format(name))
    client = hvac.Client(
        url='https://{}:{}'.format(host, port),
        verify=False)
    if client.is_sealed():
        print('Server sealed')
        client.unseal_multi(unseal_keys)
        if client.is_sealed():
            print('Server still sealed')
        else:
            print('Server unsealed')
    else:
        print('Server unsealed')

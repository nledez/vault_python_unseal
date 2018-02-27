#!/usr/bin/env python
'''
Unseal vaul servers trouth ssh tunnel
Get keys store in passwordstore as yaml
'''
import subprocess
import socket
import socks
import consul
import hvac
import yaml
import urllib3
import sys

# Disable ssl warning:
urllib3.disable_warnings()

# Use proxy socks:
socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 8585)
socket.socket = socks.socksocket


def get_config(config_type, value):
    '''
    Get config wrapper uncomment witch you want to use
    '''
    if config_type == 'passtore':
        return get_config_passtore(value)
    elif config_type == 'yaml':
        return get_config_yaml(value)  # Use this for debugging


def get_config_passtore(pass_name):
    '''
    Get config in passwordstore and convert it as yaml
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
    '''
    with open(yaml_file, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)


def get_vault_server(vault_name):
    '''
    Get vault server list in Consul
    And keep only important fields
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


def unseal(host, port, config, name=None):
    '''
    Unseal one server
    '''
    if name:
        print('{}:'.format(name))
    client = hvac.Client(
        url='https://{}:{}'.format(host, port),
        verify=False)
    if client.is_sealed():
        print('Server sealed')
        client.unseal_multi(config['unseal_keys'])
        if client.is_sealed():
            print('Server still sealed')
        else:
            print('Server unsealed')
    else:
        print('Server unsealed')


if __name__ == "__main__":
    vault_servers = get_vault_server('vault')
    # config = get_config('passtore', 'vault-test')
    # config = get_config('yaml', 'tests/vault-test.yaml')
    # config = get_config('yaml', 'tests/vault-bad-test.yaml')
    # for server in vault_servers:
    #     unseal(server['address'],
    #            server['port'],
    #            config,
    #            server['node_name'])

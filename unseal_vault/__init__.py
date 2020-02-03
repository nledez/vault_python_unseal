'''
Unseal vault servers trouth ssh tunnel
Get keys store in passwordstore as yaml
'''
import subprocess
import consul
import hvac
import json
import os
import yaml
import sys

from pprint import pprint


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
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(1)


def handle_config(config):
    if config['type'] == 'op':
        return get_config_op(config)


def get_config_op(config):
    op_check_existing_vault(config)
    uuid = op_get_item_id(config, config['op_title'])
    fields = op_get_item(config, uuid)
    return op_extract_from_item(config, fields)


def op_get_item(config, uuid):
    stream = subprocess.check_output('op get item {} --vault={}'.format(
        uuid,
        config['op_vault'],
    ),
        shell=True)
    data = json.loads(stream)

    sections = data.get('details', {}).get('sections', {})
    return op_extract_fields(sections)


def op_extract_from_item(config, fields):
    data = {}

    root_token = fields[config['op_fields_root_token']]
    unseal_keys = []
    for i in range(1, 10):
        last_value = fields.get(config['op_firlds_unseal_keys'].format(i), None)
        if last_value:
            unseal_keys.append(last_value)

    data['root_token'] = root_token
    data['unseal_keys'] = unseal_keys

    return data


def op_extract_fields(sections):
    fields_list = {}
    for section in sections:
        fields = section.get('fields', None)
        if fields:
            for field in fields:
                fields_list[field['t']] = field['v']
            return fields_list


def op_get_item_id(config, title):
    item_list = op_get_vault_item_list(config)
    return(item_list[title])


def op_get_vault_item_list(config):
    item_list = {}
    stream = subprocess.check_output('op list items --vault={}'.format(
        config['op_vault']),
        shell=True)
    data = json.loads(stream)

    for item in data:
        uuid = item['uuid']
        title = item.get('overview', {}).get('title', None)
        item_list[title] = uuid

    return item_list


def op_check_existing_vault(config):
    vault_list = []

    stream = subprocess.check_output('op list vaults', shell=True)
    data = json.loads(stream)
    for vault in data:
        vault_list.append(vault['name'])
    if config['op_vault'] not in vault_list:
        print('Need to login with:')
        print('eval `op signin {} {}`'.format(
            config['op_account_address'],
            config['op_account_email'],
        ))
        sys.exit(1)

def get_config_passtore(pass_name):
    '''
    Get config in passwordstore and convert it as yaml

    *pass_name* is the name of documents contain config
    '''
    stream = subprocess.check_output('pass show {}'.format(pass_name),
                                     shell=True)
    try:
        return yaml.load(stream, Loader=yaml.FullLoader)
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

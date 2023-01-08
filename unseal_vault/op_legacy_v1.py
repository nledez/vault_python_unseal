import json
import subprocess
import sys

from .run import run_cmd


def get_config_op_legacy_v1(config):
    op = config.get('ob_binary', 'op')
    try:
        op_legacy_check_existing_vault(config)
    except subprocess.CalledProcessError:
        print('You need to be logged with:')
        print(f'eval $({op} signin)')
        sys.exit(1)
    try:
        uuid = op_legacy_get_item_id(config, config['op_title'])
    except KeyError:
        print('Unknown config in 1password: {}'.format(config['op_title']))
        print('Config:')
        print(config)
        sys.exit(1)


    json = op_legacy_get_data(config, uuid)
    fields = op_legacy_get_item(json)
    data = op_legacy_extract_from_item(config, fields)
    if 'root_token' not in data:
        data['root_token'] = op_legacy_extract_from_password(json)
    return data


def op_legacy_get_item_id(config, title):
    item_list = op_legacy_get_vault_item_list(config)
    return(item_list[title])


def op_legacy_get_vault_item_list(config):
    op = config.get('ob_binary', 'op')
    item_list = {}
    stream = run_cmd('{} list items --vault={}'.format(
        op,
        config['op_vault']))
    data = json.loads(stream)

    for item in data:
        uuid = item['uuid']
        title = item.get('overview', {}).get('title', None)
        item_list[title] = uuid

    return item_list


def op_legacy_check_existing_vault(config):
    op = config.get('ob_binary', 'op')
    vault_list = []

    stream = run_cmd(f'{op} list vaults')
    data = json.loads(stream)
    for vault in data:
        vault_list.append(vault['name'])
    if config['op_vault'] not in vault_list:
        print('Need to login with:')
        print(f'eval $({op} signin)')
        sys.exit(1)


def op_legacy_get_data(config, uuid):
    op = config.get('ob_binary', 'op')
    stream = run_cmd('{} get item {} --vault={}'.format(
        op,
        uuid,
        config['op_vault'],
    ))
    data = json.loads(stream)
    return data


def op_legacy_get_item(data):
    sections = data.get('details', {}).get('sections', {})
    return op_legacy_extract_fields(sections)


def op_legacy_extract_fields(sections):
    fields_list = {}
    for section in sections:
        fields = section.get('fields', None)
        if fields:
            for field in fields:
                fields_list[field['t']] = field['v']
            return fields_list


def op_legacy_extract_from_item(config, fields):
    data = {}

    if 'op_fields_root_token' in config:
        data['root_token'] = fields[config['op_fields_root_token']]
    unseal_keys = []
    for i in range(1, 10):
        last_value = fields.get(config['op_firlds_unseal_keys'].format(i), None)
        if last_value:
            unseal_keys.append(last_value)

    data['unseal_keys'] = unseal_keys

    return data


def op_legacy_extract_from_password(data):
    fields = data.get('details', {}).get('fields', {})
    for field in fields:
        if field.get('name', '') == 'password':
            return field.get('value')

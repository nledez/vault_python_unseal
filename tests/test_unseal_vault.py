'''
Test unseal_vault
'''

import unseal_vault

import mock
import pytest
import yaml
import subprocess
from subprocess import CalledProcessError
from unittest.mock import MagicMock

from . import mock_content


def test_get_config():
    '''
    Test yaml load capacity
    '''
    config = unseal_vault.get_config('acme', 'tests/dot_unseal_vault.yml')
    assert isinstance(config, dict)
    with pytest.raises(SystemExit):
        unseal_vault.get_config('missing', 'tests/dot_unseal_vault.yml')
    with pytest.raises(SystemExit):
        unseal_vault.get_config('acme', 'missing-file.yaml')
    with pytest.raises(SystemExit):
        unseal_vault.get_config('acme', 'tests/bad.yml')


def test_handle_config():
    '''
    Test handle_config capacity
    '''
    mock_get_config_op = mock.patch('unseal_vault.get_config_op', autospec=True)
    with mock_get_config_op as m:
        config = {'type': 'op', 'op_vault': 'Infrastructure'}
        unseal_vault.handle_config(config)
        m.assert_called_with(config)

    mock_get_config_op = mock.patch('unseal_vault.get_config_op_legacy', autospec=True)
    with mock_get_config_op as m:
        config = {'type': 'op_legacy', 'op_vault': 'Infrastructure'}
        unseal_vault.handle_config(config)
        m.assert_called_with(config)


# def test_get_config_yaml(capsys):
#     '''
#     Test vault information in yaml file
#     '''
#     config = unseal_vault.get_config_yaml('tests/vault-test.yaml')
#     assert isinstance(config, dict)
#     assert isinstance(config['unseal_keys'], list)
#     assert config['unseal_keys'][0] == 'FoimdeegElmEctyinOssokparabBat'
#
#     with pytest.raises(SystemExit):
#         unseal_vault.get_config_yaml('tests/vault-bad-test.yaml')
#     out, err = capsys.readouterr()
#     assert out == mock_content.YAML_FILE_PARSE_ERROR
#     print(out, err)


# @mock.patch('subprocess.check_output')
# def test_get_config_passtore(mock_subproc_popen, capsys):
#     '''
#     Test vault information in passwordstore
#     '''
#     mock_subproc_popen.return_value = mock_content.YAML_CONTENT
#     config = unseal_vault.get_config_passtore('vault/test')
#     assert isinstance(config, dict)
#     assert isinstance(config['unseal_keys'], list)
#     assert config['unseal_keys'][0] == 'FoimdeegElmEctyinOssokparabBat'
#
#     with pytest.raises(SystemExit):
#         mock_subproc_popen.return_value = mock_content.YAML_BAD_CONTENT
#         unseal_vault.get_config_passtore('vault/test')
#     out, err = capsys.readouterr()
#     assert out == mock_content.YAML_CMD_PARSE_ERROR
#     print(out, err)


# @mock.patch('subprocess.check_output')
# def test_get_config(mock_subproc_popen):
#     '''
#     Test vault information in generic function
#     '''
#     mock_subproc_popen.return_value = mock_content.YAML_CONTENT
#     config = unseal_vault.get_config('passtore', 'vault/test')
#     assert isinstance(config, dict)
#     assert isinstance(config['unseal_keys'], list)
#     assert config['unseal_keys'][0] == 'FoimdeegElmEctyinOssokparabBat'
#
#     config = unseal_vault.get_config('yaml', 'tests/vault-test.yaml')
#     assert isinstance(config, dict)
#     assert isinstance(config['unseal_keys'], list)
#     assert config['unseal_keys'][0] == 'FoimdeegElmEctyinOssokparabBat'


class Consul(object):
    '''
    Consul mock
    '''
    def __init__(self, *kargs):
        '''
        Mock init
        '''
        self.catalog = Consul.Catalog(self)

    class Catalog(object):
        '''
        Mock catalog
        '''
        def __init__(self, *kargs):
            pass

        def service(name, *kargs):
            return mock_content.CONSUL_CONTENT


# def test_consul_get_vault_server(mocker):
#     '''
#     Test get vault server list in Consul
#     '''
#     mocker.patch.object(unseal_vault.consul, 'Consul', Consul)
#     vault_servers = unseal_vault.consul_get_vault_server('vault')
#     assert isinstance(vault_servers, list)
#     assert len(vault_servers) == 3
#     assert vault_servers == [
#         {'address': '192.168.1.1', 'node_name': 'consul-01', 'port': 8200},
#         {'address': '192.168.1.2', 'node_name': 'consul-02', 'port': 8200},
#         {'address': '192.168.1.3', 'node_name': 'consul-03', 'port': 8200},
#         ]

'''
Test unseal_vault
'''

import unseal_vault

import mock
import pytest
import yaml
import httpretty
from unittest.mock import MagicMock

from . import mock_content



def test_get_config_yaml(capsys):
    config = unseal_vault.get_config_yaml('tests/vault-test.yaml')
    assert isinstance(config, dict)
    assert isinstance(config['unseal_keys'], list)
    assert config['unseal_keys'][0] == 'FoimdeegElmEctyinOssokparabBat'

    with pytest.raises(SystemExit):
        unseal_vault.get_config_yaml('tests/vault-bad-test.yaml')
    out, err = capsys.readouterr()
    assert out == mock_content.YAML_FILE_PARSE_ERROR
    print(out, err)


@mock.patch('subprocess.check_output')
def test_get_config_passtore(mock_subproc_popen, capsys):
    mock_subproc_popen.return_value = mock_content.YAML_CONTENT
    config = unseal_vault.get_config_passtore('vault/test')
    assert isinstance(config, dict)
    assert isinstance(config['unseal_keys'], list)
    assert config['unseal_keys'][0] == 'FoimdeegElmEctyinOssokparabBat'

    with pytest.raises(SystemExit):
        mock_subproc_popen.return_value = mock_content.YAML_BAD_CONTENT
        unseal_vault.get_config_passtore('vault/test')
    out, err = capsys.readouterr()
    assert out == mock_content.YAML_CMD_PARSE_ERROR
    print(out, err)


@mock.patch('subprocess.check_output')
def test_get_config(mock_subproc_popen):
    mock_subproc_popen.return_value = mock_content.YAML_CONTENT
    config = unseal_vault.get_config('passtore', 'vault/test')
    assert isinstance(config, dict)
    assert isinstance(config['unseal_keys'], list)
    assert config['unseal_keys'][0] == 'FoimdeegElmEctyinOssokparabBat'

    config = unseal_vault.get_config('yaml', 'tests/vault-test.yaml')
    assert isinstance(config, dict)
    assert isinstance(config['unseal_keys'], list)
    assert config['unseal_keys'][0] == 'FoimdeegElmEctyinOssokparabBat'


class Consul(object):
    def __init__(self, *kargs):
        self.catalog = Consul.Catalog(self)

    def __str__(self):
        return 'Consul Mock'

    class Catalog(object):
        def __init__(self, *kargs):
            pass

        def service(name, *kargs):
            return mock_content.CONSUL_CONTENT


def test_get_vault_server(mocker):
    mocker.patch.object(unseal_vault.consul, 'Consul', Consul)
    vault_servers = unseal_vault.get_vault_server('vault')
    assert isinstance(vault_servers, list)
    assert len(vault_servers) == 3
    assert vault_servers == [
        {'address': '192.168.1.1', 'node_name': 'consul-01', 'port': 8200},
        {'address': '192.168.1.2', 'node_name': 'consul-02', 'port': 8200},
        {'address': '192.168.1.3', 'node_name': 'consul-03', 'port': 8200},
        ]


class HvacClient(object):
    def __init__(self, **kargs):
        self.sealed = True

    def __str__(self):
        return 'Vault Mock'

    def is_sealed(self):
        return self.sealed

    def unseal_multi(self, *kargs):
        return self.sealed


def test_get_unseal(mocker):
    mocker.patch.object(unseal_vault.hvac, 'Client', HvacClient)
    server = mock_content.UNSEAL_CONFIG[0]
    config = unseal_vault.get_config_yaml('tests/vault-test.yaml')
    unseal_vault.unseal(server['address'],
                        server['port'],
                        config,
                        server['node_name'])

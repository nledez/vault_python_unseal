"""
Test unseal_vault
"""

import os
from unittest.mock import patch

import pytest

import unseal_vault
from tests import mock_content

TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def test_get_config():
    """
    Test yaml load capacity
    """
    config = unseal_vault.get_config("acme", f"{TEST_DIR}/dot_unseal_vault.yml")
    assert isinstance(config, dict)
    with pytest.raises(SystemExit):
        unseal_vault.get_config("missing", f"{TEST_DIR}/dot_unseal_vault.yml")
    with pytest.raises(SystemExit):
        unseal_vault.get_config("acme", "missing-file.yaml")
    with pytest.raises(SystemExit):
        unseal_vault.get_config("acme", f"{TEST_DIR}/bad.yml")


# def test_handle_config():
#     """
#     Test handle_config capacity
#     """
#     mock_get_config_op = patch("unseal_vault.get_config_op_v1", autospec=True)
#     with mock_get_config_op as m:
#         config = {"type": "op_v1", "op_vault": "Infrastructure"}
#         unseal_vault.handle_config(config)
#         m.assert_called_with(config)
#
#     mock_get_config_op = patch("unseal_vault.get_config_op_v2", autospec=True)
#     with mock_get_config_op as m:
#         config = {"type": "op_v2", "op_vault": "Infrastructure"}
#         unseal_vault.handle_config(config)
#         m.assert_called_with(config)


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


# @patch('subprocess.check_output')
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


# @patch('subprocess.check_output')
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
    """
    Consul mock
    """

    def __init__(self, *kargs):
        """
        Mock init
        """
        self.catalog = Consul.Catalog(self)

    class Catalog(object):
        """
        Mock catalog
        """

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

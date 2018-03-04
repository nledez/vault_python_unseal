'''
Test unseal_vault.config
'''

import unseal_vault.config

import mock
import pytest

from . import mock_content


def missing_config(filename):
    return False


def test_missing_config_file(capsys):
    patcher_exists = mock.patch('os.path.exists')
    mock_exists = patcher_exists.start()
    mock_exists.side_effect = missing_config
    with pytest.raises(SystemExit):
        unseal_vault.config.load()
    out, err = capsys.readouterr()
    assert out == 'Missing ~/.unseal_vault.yml file. Please create it.\n'
    print(out, err)


def exist_config(filename):
    if filename == '~/.unseal_vault.yml':
        return True
    else:
        return False


def test_bad_config_file(capsys):
    patcher_exists = mock.patch('os.path.exists')
    mock_exists = patcher_exists.start()
    mock_exists.side_effect = exist_config

    config_content = ''.join(open('tests/vault-bad-test.yaml').readlines())

    with mock.patch('unseal_vault.config.open',
                    mock.mock_open(read_data=config_content),
                    create=True) as m:
        with pytest.raises(SystemExit):
            unseal_vault.config.load()
        m.assert_called_once_with(unseal_vault.config.CONFIG_PATH, 'r')
        out, err = capsys.readouterr()
        assert out.split('\n')[:-2] == mock_content.YAML_FILE_PARSE_ERROR.split('\n')[:-2]
        print(out, err)


def test_open_config_file():
    patcher_exists = mock.patch('os.path.exists')
    mock_exists = patcher_exists.start()
    mock_exists.side_effect = exist_config

    config_content = ''.join(open('tests/config.yml').readlines())

    with mock.patch('unseal_vault.config.open',
                    mock.mock_open(read_data=config_content),
                    create=True) as m:
        config = unseal_vault.config.load()
        m.assert_called_once_with(unseal_vault.config.CONFIG_PATH, 'r')
        assert isinstance(config, dict)
        assert sorted(list(config.keys())) == ['vault-consul-passwdstore',
                                               'vault-yaml']


def test_open_config_file():
    patcher_exists = mock.patch('os.path.exists')
    mock_exists = patcher_exists.start()
    mock_exists.side_effect = exist_config

    config_content = ''.join(open('tests/config.yml').readlines())

    with mock.patch('unseal_vault.config.open',
                    mock.mock_open(read_data=config_content),
                    create=True) as m:
        config = unseal_vault.config.load()
        m.assert_called_once_with(unseal_vault.config.CONFIG_PATH, 'r')
        assert isinstance(config, dict)
        assert list(config.keys()) == ['vault-yaml',
                                       'vault-consul-passwdstore']

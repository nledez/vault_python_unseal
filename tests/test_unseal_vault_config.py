'''
Test unseal_vault.config
'''

import mock
import pytest

import unseal_vault.config

from . import mock_content


def missing_config(filename):
    '''
    Mock missing config file
    '''
    return False


def test_missing_config_file(capsys):
    '''
    Test missing config file
    '''
    patcher_exists = mock.patch('os.path.exists')
    mock_exists = patcher_exists.start()
    mock_exists.side_effect = missing_config
    with pytest.raises(SystemExit):
        unseal_vault.config.load()
    out, err = capsys.readouterr()
    assert out == 'Missing ~/.unseal_vault.yml file. Please create it.\n'
    print(out, err)


def exist_config(filename):
    '''
    Mock config file exist
    '''
    return filename == '~/.unseal_vault.yml'


def test_bad_config_file(capsys):
    '''
    Test bad config yaml file
    '''
    patcher_exists = mock.patch('os.path.exists')
    mock_exists = patcher_exists.start()
    mock_exists.side_effect = exist_config

    config_content = ''.join(open('tests/vault-bad-test.yaml').readlines())

    with mock.patch('unseal_vault.config.open',
                    mock.mock_open(read_data=config_content),
                    create=True) as m_open:
        with pytest.raises(SystemExit):
            unseal_vault.config.load()
        m_open.assert_called_once_with(unseal_vault.config.CONFIG_PATH, 'r')
        out, err = capsys.readouterr()
        out_without_filename = out.split('\n')[:-2]
        assert_wo_fn = mock_content.YAML_FILE_PARSE_ERROR.split('\n')[:-2]
        assert out_without_filename == assert_wo_fn
        print(out, err)


def test_open_config_file():
    '''
    Test config yaml file
    '''
    patcher_exists = mock.patch('os.path.exists')
    mock_exists = patcher_exists.start()
    mock_exists.side_effect = exist_config

    config_content = ''.join(open('tests/config.yml').readlines())

    with mock.patch('unseal_vault.config.open',
                    mock.mock_open(read_data=config_content),
                    create=True) as m_open:
        config = unseal_vault.config.load()
        m_open.assert_called_once_with(unseal_vault.config.CONFIG_PATH, 'r')
        assert isinstance(config, dict)
        assert sorted(list(config.keys())) == ['vault-consul-passwdstore',
                                               'vault-yaml']

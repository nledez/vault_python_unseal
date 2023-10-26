import pytest

import unseal_vault.vault

from . import mock_content


class HvacSys(object):
    def __init__(self, **kargs):
        self.sealed = True

    def is_sealed(self):
        return self.sealed

    def submit_unseal_keys(self, *args, **kwargs):
        # Implement the mock behavior for submit_unseal_keys
        # For example, if submitting the keys is supposed to unseal the vault,
        # you might want to set self.sealed to False.
        self.sealed = False
        return self.sealed


class HvacClient(object):
    '''
    Mock Vault client
    '''
    def __init__(self, **kargs):
        self.sealed = True
        self._sys = HvacSys()

    @property
    def sys(self):
        return self._sys

    def __str__(self):
        return 'Vault Mock'

    def unseal_multi(self, *kargs):
        self.sealed = False
        return self.sealed


def test_sealed_get_unseal(capsys, mocker):
    '''
    Test unseal Vault
    '''
    mocker.patch.object(unseal_vault.vault.hvac, 'Client', HvacClient)
    server = mock_content.UNSEAL_CONFIG[0]
    config = {
        'unseal_keys': [
            'FoimdeegElmEctyinOssokparabBat',
            'saikTaDronjosBick2flalvEcVinus',
            'ThooshpAbpajWuIjwawbulgIfteak9',
            'OisckInudgiOkarUfNuWeogCemReds',
            'eivHowadGowJoQuadevedViedcyal3',
        ]
    }

    unseal_vault.vault.unseal('https',
                              server['address'],
                              server['port'],
                              config['unseal_keys'],
                              server['node_name'])
    captured = capsys.readouterr()
    assert captured.out == mock_content.SEALED_STDOUT


class UnsealedHvacClient(HvacClient):
    def __init__(self, **kargs):
        self.sealed = False


# def test_unsealed_get_unseal(capsys, mocker):
#     '''
#     Test unseal Vault allready unsealed
#     '''
#     mocker.patch.object(unseal_vault.hvac, 'Client', UnsealedHvacClient)
#     server = mock_content.UNSEAL_CONFIG[0]
#     config = unseal_vault.get_config_yaml('tests/vault-test.yaml')
#     unseal_vault.vault.unseal(server['address'],
#                         server['port'],
#                         config['unseal_keys'],
#                         server['node_name'])
#     captured = capsys.readouterr()
#     assert captured.out == mock_content.UNSEALED_STDOUT


class StillSealedHvacClient(HvacClient):
    def unseal_multi(self, *kargs):
        self.sealed = True
        return self.sealed


# def test_still_sealed_get_unseal(capsys, mocker):
#     '''
#     Test unseal Vault can't unsealed
#     '''
#     mocker.patch.object(unseal_vault.hvac, 'Client', StillSealedHvacClient)
#     server = mock_content.UNSEAL_CONFIG[0]
#     config = unseal_vault.get_config_yaml('tests/vault-test.yaml')
#     unseal_vault.vault.unseal(server['address'],
#                         server['port'],
#                         config['unseal_keys'],
#                         server['node_name'])
#     captured = capsys.readouterr()
#     assert captured.out == mock_content.STILL_SEALED_STDOUT

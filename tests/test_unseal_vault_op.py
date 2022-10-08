'''
Test unseal_vault.op
'''
import mock
import pytest
import subprocess

import unseal_vault.op


def test_op_check_existing_vault():
    '''
    Test op_check_existing_vault capacity
    '''
    mock_run_cmd = mock.patch('unseal_vault.op.run_cmd', autospec=True)
    with mock_run_cmd as m:
        m.return_value = b'[{"id": "xxxxx", "name": "Infrastructure", "content_version": 181}]'
        config = {'op_vault': 'Infrastructure'}
        unseal_vault.op.op_check_existing_vault(config)
        assert m.called is True

    with pytest.raises(SystemExit):
        mock_run_cmd = mock.patch('unseal_vault.op.run_cmd', autospec=True)
        with mock_run_cmd as m:
            m.return_value = b'[{"id": "xxxxx", "name": "Infrastructure", "content_version": 181}]'
            config = {'op_vault': 'Missing'}
            unseal_vault.op.op_check_existing_vault(config)
            assert m.called is True

    with pytest.raises(SystemExit):
        mock_run_cmd = mock.patch('unseal_vault.op.run_cmd', autospec=True)
        with mock_run_cmd as m:
            m.side_effect = subprocess.CalledProcessError(1, '')
            config = {'op_vault': 'Infrastructure'}
            unseal_vault.op.op_check_existing_vault(config)
            assert m.called is True

    with pytest.raises(SystemExit):
        config = {}
        unseal_vault.op.op_check_existing_vault(config)
        assert m.called is True

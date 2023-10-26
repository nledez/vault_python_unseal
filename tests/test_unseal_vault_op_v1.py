"""
Test unseal_vault.op_v1
"""
import subprocess
from unittest.mock import patch

import pytest

import unseal_vault.op_v1


@patch("unseal_vault.op_v1.run_cmd", autospec=True)
def test_op_check_existing_vault(mock_run_cmd):
    """
    Test op_check_existing_vault capacity
    """
    mock_run_cmd.return_value = (
        b'[{"id": "xxxxx", "name": "Infrastructure", "content_version": 181}]'
    )
    config = {"op_vault": "Infrastructure"}
    unseal_vault.op_v1.op_check_existing_vault(config)
    assert mock_run_cmd.called is True

    with pytest.raises(SystemExit):
        mock_run_cmd.return_value = (
            b'[{"id": "xxxxx", "name": "Infrastructure", "content_version": 181}]'
        )
        config = {"op_vault": "Missing"}
        unseal_vault.op_v1.op_check_existing_vault(config)
        assert mock_run_cmd.called is True

    with pytest.raises(SystemExit):
        mock_run_cmd.side_effect = subprocess.CalledProcessError(1, "")
        config = {"op_vault": "Infrastructure"}
        unseal_vault.op_v1.op_check_existing_vault(config)
        assert mock_run_cmd.called is True

    with pytest.raises(SystemExit):
        config = {}
        unseal_vault.op_v1.op_check_existing_vault(config)
        assert mock_run_cmd.called is True

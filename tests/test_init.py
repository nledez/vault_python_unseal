import pytest
from unittest.mock import mock_open, patch
import unseal_vault


@patch("os.path.exists", return_value=False)
def test_get_config_missing_file(os_path_exists, capsys):
    with pytest.raises(SystemExit):
        unseal_vault.get_config("missing_config", "wrong_path")
    captured = capsys.readouterr()
    assert "Missing" in captured.err

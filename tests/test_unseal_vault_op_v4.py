"""
Test unseal_vault.op_v4
"""
import pytest
import subprocess
from unittest.mock import patch
import unseal_vault.op_v4 as op_v4


@patch("unseal_vault.op_v4.run_cmd", autospec=True)
def test_os_get_item_entry(mock_run_cmd):
    mock_run_cmd.return_value = b"hvs.sIRzLMhcvEif0pfGMgZ4QwXG"
    root_token = op_v4.os_get_item_entry(
        {}, "op://SecurityTeam/Ahxeitheimifeeh2Ahmai3iarei/password"
    )
    assert root_token == "hvs.sIRzLMhcvEif0pfGMgZ4QwXG"

    mock_run_cmd.return_value = b"4oa9HuS7au4hyljXjnIF6ilhpF+/OCwq49vCIYOjZVA="

    unseal_key_1 = op_v4.os_get_item_entry(
        {}, "op://SecurityTeam/Ahxeitheimifeeh2Ahmai3iarei/Unseal Key 1"
    )
    assert unseal_key_1 == "4oa9HuS7au4hyljXjnIF6ilhpF+/OCwq49vCIYOjZVA="

    with pytest.raises(op_v4.UnknownItemError):
        mock_run_cmd.side_effect = subprocess.CalledProcessError(1, "op")
        unseal_key_2 = op_v4.os_get_item_entry(
            {}, "op://SecurityTeam/Ahxeitheimifeeh2Ahmai3iarei/Unseal Key 2"
        )
        assert unseal_key_2 == ""


@pytest.fixture
def sample_config():
    return {
        "op_root_token": "op://SecurityTeam/Ahxeitheimifeeh2Ahmai3iarei/password",
        "op_unseal_keys": "op://SecurityTeam/Ahxeitheimifeeh2Ahmai3iarei/Unseal Key {}",
        "op_fields_unseal_keys_count": 3,
        "ob_binary": "op",
    }


@patch("unseal_vault.op_v4.os_get_item_entry")
def test_get_config_op_v4_with_all_keys(mock_get_item, sample_config):
    expected_values = [
        "root_token_value",
        "unseal_key_1",
        "unseal_key_2",
        "unseal_key_3",
    ]
    mock_get_item.side_effect = expected_values

    result = op_v4.get_config_op_v4(sample_config)

    # Assertions
    assert result["root_token"] == "root_token_value"
    assert result["unseal_keys"] == expected_values[1:]

    # Verify call counts
    total_calls = 1 + sample_config["op_fields_unseal_keys_count"]
    assert mock_get_item.call_count == total_calls

    # Verify call arguments
    mock_get_item.assert_any_call(sample_config, sample_config["op_root_token"])
    for i in range(1, sample_config["op_fields_unseal_keys_count"] + 1):
        key_path = sample_config["op_unseal_keys"].format(i)
        mock_get_item.assert_any_call(sample_config, key_path)


@pytest.mark.skip("WIP")
@patch("unseal_vault.op_v4.run_cmd", side_effect=subprocess.CalledProcessError(1, "op"))
def test_get_config_op_v4_with_failed_keys(mock_run_cmd, sample_config):
    expected_unseal_keys = []

    result = op_v4.get_config_op_v4(sample_config)

    assert result["root_token"] is None
    assert result["unseal_keys"] == expected_unseal_keys


@pytest.mark.skip("WIP")
@patch("unseal_vault.op_v4.run_cmd", return_value=b"")
def test_get_config_op_v4_with_empty_keys(mock_run_cmd, sample_config):
    expected_unseal_keys = []

    result = op_v4.get_config_op_v4(sample_config)

    assert result["root_token"] == ""
    assert result["unseal_keys"] == expected_unseal_keys

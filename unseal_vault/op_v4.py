import json
import subprocess

from .run import run_cmd


class UnknownItemError(Exception):
    pass


def os_get_item_entry(config, path):
    op = config.get("ob_binary", "op")
    try:
        stream = run_cmd(f'{op} read "{path}"')
    except subprocess.CalledProcessError:
        raise UnknownItemError(f"Unknown item {path}")
    data = stream.decode().rstrip("\n")

    return data


def get_config_op_v4(config):
    data = {}

    data["root_token"] = os_get_item_entry(config, config["op_root_token"])

    unseal_keys = []
    op_fields_unseal_keys_count = config.get("op_fields_unseal_keys_count", 1)
    for i in range(1, op_fields_unseal_keys_count + 1):
        try:
            last_value = os_get_item_entry(config, config["op_unseal_keys"].format(i))
            if last_value:
                unseal_keys.append(last_value)
        except subprocess.CalledProcessError:
            pass

    data["unseal_keys"] = unseal_keys

    return data

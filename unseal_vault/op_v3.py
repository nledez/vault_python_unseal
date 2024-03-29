import json
import subprocess
import sys

from .run import run_cmd


def op_check_existing_vault(config):
    op = config.get("ob_binary", "op")
    try:
        vault_name = config["op_vault"]
    except KeyError as e:
        if str(e) == "'op_vault'":
            print("Bad config:")
            print("eval $(config)")
            sys.exit(1)
    try:
        vault_list = []

        stream = run_cmd(f"{op} vault list --format=json")
        data = json.loads(stream)
        for vault in data:
            vault_list.append(vault["name"])
        if vault_name not in vault_list:
            print(f'Missing "{vault_name}" vault')
            print("May need to login with:")
            print(f"eval $({op} signin)")
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("You need to be logged with:")
        print(f"eval $({op} signin)")
        sys.exit(1)


def get_config_op_v3(config):
    op_check_existing_vault(config)

    data = {}

    data["root_token"] = os_get_item_entry(config, config["op_title"], "password")

    unseal_keys = []
    op_fields_unseal_keys_count = config.get("op_fields_unseal_keys_count", 1)
    for i in range(1, op_fields_unseal_keys_count + 1):
        try:
            last_value = os_get_item_entry(
                config, config["op_title"], config["op_firlds_unseal_keys"].format(i)
            )
            if last_value:
                unseal_keys.append(last_value)
        except subprocess.CalledProcessError:
            pass

    data["unseal_keys"] = unseal_keys

    return data


def os_get_item_entry(config, title, entry_name):
    op = config.get("ob_binary", "op")
    stream = run_cmd(f'{op} read "op://{config["op_vault"]}/{title}/{entry_name}"')
    data = stream.decode().rstrip("\n")

    return data

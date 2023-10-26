"""
Unseal vault servers through ssh tunnel
Get keys store in passwordstore as yaml
"""
import os
import sys

import yaml

from .op_v1 import get_config_op_v1
from .op_v2 import get_config_op_v2
from .op_v3 import get_config_op_v3
from .op_v4 import get_config_op_v4


def get_config(config_name, yaml_file="~/.unseal_vault.yml"):
    """
    Get config wrapper

    *config_type* need to be defined as 'passtore' or 'yaml'

    *path* the pass to get yaml configuration
    """

    full_path = os.path.expanduser(yaml_file)
    if not os.path.exists(full_path):
        print("Missing {} file. Please create it.".format(full_path))
        sys.exit(1)
    else:
        with open(full_path, "r") as stream:
            try:
                return yaml.load(stream, Loader=yaml.FullLoader)[config_name]
            except KeyError as k:
                print(f"Missing config: {k}")
                sys.exit(1)
            except yaml.YAMLError as exc:
                print(exc)
                sys.exit(1)


def handle_config(config):
    if config["type"] == "op_v1":
        return get_config_op_v1(config)
    if config["type"] == "op_v2":
        return get_config_op_v2(config)
    if config["type"] == "op_v3":
        return get_config_op_v3(config)
    if config["type"] == "op_v4":
        return get_config_op_v4(config)

import sys

import yaml

from unseal_vault.run import run_cmd


def get_config_passtore(pass_name):
    """
    Get config in passwordstore and convert it as yaml

    *pass_name* is the name of documents contain config
    """
    stream = run_cmd(f"pass show {pass_name}")
    try:
        return yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit(1)

#!/usr/bin/env python

from unseal_vault import consul_get_vault_server, handle_config, get_config, unseal
import socket
import socks
import urllib3

from pprint import pprint

# Disable ssl warning:
urllib3.disable_warnings()

# Use proxy socks:
socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 8585)
socket.socket = socks.socksocket

config = get_config('demo')
pprint(handle_config(config))

# vault_servers = consul_get_vault_server('vault')
# config = get_config('passtore', 'vault-test')
# config = get_config('yaml', 'tests/vault-test.yaml')
# config = get_config('yaml', 'tests/vault-bad-test.yaml')
# for server in vault_servers:
#     unseal(server['address'],
#            server['port'],
#            config['unseal_keys'],
#            server['node_name'])

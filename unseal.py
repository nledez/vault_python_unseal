#!/usr/bin/env python

from unseal_vault import handle_config, get_config
from unseal_vault.consul import consul_get_vault_server
from unseal_vault.vault import unseal
import subprocess
import socket
import socks
import urllib3
import sys

if len(sys.argv) <= 1:
    print('Must have a cluster in argument:')
    print('{} <cluster>'.format(sys.argv[0]))
    sys.exit(1)
cluster = sys.argv[1]
print('Unseal cluster: {}'.format(cluster))

# Disable ssl warning:
urllib3.disable_warnings()

config = get_config(cluster)
for k, v in handle_config(config).items():
    config[k] = v

if len(config['unseal_keys']) == 0:
    print('unseal_keys is empty, may check parameter in config file')
    sys.exit(1)


if 'consul_port' not in config:
    config['consul_port'] = '8500'
if 'consul_scheme' not in config:
    config['consul_scheme'] = 'http'

# Use proxy socks:
socks.set_default_proxy(socks.SOCKS5,
                        config['proxy_sock_host'],
                        config['proxy_sock_port'],
                        True)
socket.socket = socks.socksocket

# Launch background ssh
print('Connect with: {}'.format(config['ssh_command']))
stream = subprocess.Popen(config['ssh_command'], shell=True)
stream.communicate()

print('Connect to Consul:')
vault_servers = consul_get_vault_server('vault',
                                        consul_host=config['consul_host'],
                                        consul_port=config['consul_port'],
                                        consul_scheme=config['consul_scheme'],
                                        )

for server in vault_servers:
    unseal(config['vault_scheme'],
           server['address'],
           8200,
           config['unseal_keys'],
           server['node_name'])

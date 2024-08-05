"""
All mocks data here
"""

YAML_CONTENT = "---\nunseal_keys:\n  - FoimdeegElmEctyinOssokparabBat"

YAML_FILE_PARSE_ERROR = """while parsing a flow node
expected the node content, but found '<stream end>'
  in "tests/vault-bad-test.yaml", line 2, column 1
"""

YAML_BAD_CONTENT = "[ ["
YAML_CMD_PARSE_ERROR = """while parsing a flow node
expected the node content, but found '<stream end>'
  in "<unicode string>", line 1, column 4:
    [ [
       ^
"""

CONSUL_CONTENT = [
    41,
    [
        {
            "Address": "192.168.1.1",
            "Node": "consul-01",
            "ServiceAddress": "192.168.1.1",
            "ServicePort": 8200,
        },
        {
            "Address": "192.168.1.2",
            "Node": "consul-02",
            "ServiceAddress": "192.168.1.2",
            "ServicePort": 8200,
        },
        {
            "Address": "192.168.1.3",
            "Node": "consul-03",
            "ServiceAddress": "192.168.1.3",
            "ServicePort": 8200,
        },
    ],
]

UNSEAL_CONFIG = [
    {"address": "192.168.1.1", "node_name": "consul-01", "port": 8200},
    {"address": "192.168.1.2", "node_name": "consul-02", "port": 8200},
    {"address": "192.168.1.3", "node_name": "consul-03", "port": 8200},
]

SEALED_STDOUT = """Connect to URL: https://192.168.1.1:8200
consul-01:
Server sealed
Server unsealed
"""

UNSEALED_STDOUT = """consul-01:
Server unsealed
"""

STILL_SEALED_STDOUT = """consul-01:
Server sealed
Server still sealed
"""

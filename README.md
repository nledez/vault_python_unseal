[![Build Status](https://travis-ci.org/nledez/vault_python_unseal.svg?branch=master)](https://travis-ci.org/nledez/vault_python_unseal) [![Coverage Status](https://coveralls.io/repos/github/nledez/vault_python_unseal/badge.svg)](https://coveralls.io/github/nledez/vault_python_unseal)
# Install:

```
virtualenv -p python3 venv
./venv/bin/pip install -r requirements.txt
```

# Launch SSH Proxy socks:

```
ssh -D 8585 consul-server
```

# Unseal all node in cluster:

```
./venv/bin/python unseal.py
```

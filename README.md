Python helper for unseal [Vault.io](http://vaultproject.io/) cluster.

## Status

[![Build Status](https://github.com/nledez/vault_python_unseal/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/nledez/vault_python_unseal/actions/workflows/tests.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nledez/vault_python_unseal/master.svg)](https://results.pre-commit.ci/latest/github/nledez/vault_python_unseal/master)
[![Coverage Status](https://img.shields.io/coveralls/nledez/vault_python_unseal.svg?style=flat-square)](https://coveralls.io/r/nledez/vault_python_unseal?branch=master)
[![Read the doc Status](https://readthedocs.org/projects/vault-python-unseal/badge/?version=latest)](http://vault-python-unseal.readthedocs.io/)

## Install

```
virtualenv -p python3 .venv
./.venv/bin/pip install -r requirements.txt
```

## Launch SSH Proxy socks

```
ssh -D 8585 consul-server
```

## Unseal all node in cluster

```
./.venv/bin/python unseal.py
```

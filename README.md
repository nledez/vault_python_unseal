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

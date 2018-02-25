virtualenv -p python3 venv
./venv/bin/pip install -r requirements.txt

# In another terminal:
ssh -D 8585 consul-server

./venv/bin/python unseal.py

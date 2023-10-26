Python helper for unseal `Vault.io <http://vaultproject.io/>`_

Status
------

|Build Status|\ |Coverage Status|\ |Read the doc Status|

.. |Build Status|
   image:: https://github.com/nledez/vault_python_unseal/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/nledez/vault_python_unseal/actions/workflows/tests.yml
.. |Coverage Status|
   image:: https://img.shields.io/coveralls/nledez/vault_python_unseal.svg?style=flat-square
   :target: https://coveralls.io/r/nledez/vault_python_unseal?branch=master
.. |Read the doc Status|
   image:: https://readthedocs.org/projects/vault-python-unseal/badge/?version=latest
   :target: http://vault-python-unseal.readthedocs.io/

Install
-------

.. code:: bash

        virtualenv -p python3 .venv
        ./.venv/bin/pip install -r requirements.txt

Launch SSH Proxy socks
----------------------

.. code:: bash

        ssh -D 8585 consul-server

Unseal all node in cluster
--------------------------

.. code:: bash

        ./.venv/bin/python unseal.py

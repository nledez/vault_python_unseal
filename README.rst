Python helper for unseal `Vault.io <http://vaultproject.io/>`_

Status
------

|Build Status|\ |Coverage Status|

.. |Build Status|
   image:: https://img.shields.io/travis/nledez/vault_python_unseal.svg?style=flat-square
   :target: https://travis-ci.org/nledez/vault_python_unseal
.. |Coverage Status|
   image:: https://img.shields.io/coveralls/nledez/vault_python_unseal.svg?style=flat-square
   :target: https://coveralls.io/r/nledez/vault_python_unseal?branch=master

Install
-------

.. code:: bash

        virtualenv -p python3 venv
        ./venv/bin/pip install -r requirements.txt

Launch SSH Proxy socks
----------------------

.. code:: bash

        ssh -D 8585 consul-server

Unseal all node in cluster
--------------------------

.. code:: bash

        ./venv/bin/python unseal.py

test:
	tox

clean:
	rm -rf dist vault_unseal.egg-info .coverage

distclean: clean
	rm -rf build venv .eggs .tox

package:
	python setup.py sdist

.PHONY: clean package publish

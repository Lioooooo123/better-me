PYTHON ?= python3

.PHONY: check validate test upstream status

check: validate test

validate:
	$(PYTHON) scripts/validate.py

test:
	$(PYTHON) -m unittest discover -s tests -v

upstream:
	$(PYTHON) scripts/check_upstream.py --skills

status:
	$(PYTHON) scripts/manage.py status

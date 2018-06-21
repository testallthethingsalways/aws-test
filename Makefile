VIRTUALENV = .venv/aws
ACTIVATE = $(VIRTUALENV)/bin/activate

# If a virtualenv is not already existing, create it
venv-setup:
	test -d "$(VIRTUALENV)" || virtualenv -p `which python3` "$(VIRTUALENV)"

# Activate the virtualenv and install the dependencies
devbuild: venv-setup
	. $(ACTIVATE) && pip install -e .
	@echo "Run '. .venv/load/bin/activate' to enter the virtualenv"

# Run controller scripts to start instances
test-api: devbuild lint
	. $(ACTIVATE) && pytest tests

lint:
	pycodestyle aws/
	flake8 aws/
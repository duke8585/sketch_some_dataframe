# inspired by https://github.com/idealo/shalmaneser-parquet-file-merge/blob/main/Makefile
# and https://github.com/idealo/die-monte-carlo-dq/blob/main/Makefile

PYTHON = python3
PYTHON_VERSION = 3.9.13
VENV = .venv
APP_NAME = "idealo-dl-landscape"

.PHONY: all
DEFAULT_GOAL: generate

setup: get_pyenv venv

venv: $(VENV)/touchfile # wrapper for the one below

get_pyenv:
	@echo "installing pyenv via homebrew and python$(PYENV_VERSION)"
	brew install pyenv
	pyenv install -v $(PYENV_VERSION) || true # to avoid cancelling the recipe if existing

# only when requirements change: https://stackoverflow.com/questions/24736146/how-to-use-virtualenv-in-makefile
$(VENV)/touchfile: requirements.txt requirements-dev.txt
	export PYENV_VERSION="$(PYTHON_VERSION)"
	@echo "Creating virtual environment and installing dependencies"
	$(PYTHON) -m venv $(VENV) || { echo "!!!no $(PYTHON) found"; exit 1; }
	. $(VENV)/bin/activate && pip install --upgrade pip \
	&& pip install -r requirements.txt && pip install -r requirements-dev.txt
	@touch $(VENV)/touchfile


update: # to force the upper
	. $(VENV)/bin/activate && pip install --upgrade pip \
	&& pip install -r requirements.txt && pip install -r requirements-dev.txt

cleanup:
	@echo "Cleaning up the envs / temps."
	@rm -rf $(VENV)/
	# TODO more to be deleted?

generate:
	python main.py

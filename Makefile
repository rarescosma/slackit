PROJECT:=slackit
SHELL:=/bin/bash
MK_PATH:=$(abspath $(lastword $(MAKEFILE_LIST)))
MK_DIR:=$(dir $(MK_PATH))
BINDIR?=/usr/bin

# Needed to make pyinstaller play nice
GAPI_CLIENT_PKG=google_api_python_client-1.12.3.dist-info

default: dist

help:
	@echo 'Usage: make [target] ...'
	@echo
	@echo 'Targets:'
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep  \
	| sed -e 's/^\(.*\):[^#]*#\(.*\)/\1 \2/' | tr '#' "\t"

test:  ### Test code quality
	black -l 80 --check $(PROJECT)
	isort -l80 -m3 --tc --check-only $(PROJECT)
	mypy $(PROJECT)
	pylint $(PROJECT)

dist: dist/$(PROJECT) ### Build a one-file executable

dist/$(PROJECT): .venv/freeze var/$(GAPI_CLIENT_PKG)
	. .venv/bin/activate && pyinstaller installer.spec

install: dist/$(PROJECT)  ## Install the executable
	install -m 755 dist/$(PROJECT) $(BINDIR)

clean:  ### Clean up everything
	rm -rf dist build __pycache__ *.egg-info .python-version .venv

var/$(GAPI_CLIENT_PKG): .venv/freeze
	mkdir -p $(MK_DIR)var
	ln -sf $(MK_DIR).venv/lib/python3.8/site-packages/$(GAPI_CLIENT_PKG) \
	  $(MK_DIR)var/$(GAPI_CLIENT_PKG)

.python-version:
	pyenv local 3.8.6

.venv/freeze: .python-version  ## Create a virtual environment under '.venv'
	test -f .venv/bin/activate || python3 -mvenv .venv --prompt $(PROJECT)
	. .venv/bin/activate && pip install -e . && pip freeze > .venv/freeze

.PHONY: help clean dist install

.PHONY: run run_tests unzip

# Get the root directory of the project (where this Makefile is)
ROOT_DIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))

run:
	cd $(ROOT_DIR) && PYTHONPATH=. streamlit run app/app_launch.py

run_tests:
	cd $(ROOT_DIR)/tests && PYTHONPATH=$(ROOT_DIR) pytest

unzip:
	cd $(ROOT_DIR)/src && PYTHONPATH=$(ROOT_DIR) python3 unzip.py

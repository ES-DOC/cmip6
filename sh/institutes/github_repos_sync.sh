#!/bin/bash

# Main entry point.
main()
{
	activate_venv

	pipenv run python $CMIP6_LIB/institutes/github_repos_sync.py
}

# Invoke entry point.
main

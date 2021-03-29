#!/usr/bin/env bash

# Main entry point.
function _main()
{
	if [ "$1" ]; then
		institution=$1
	else
		institution=all
	fi

	xls_template=$CMIP6_HOME/lib/citations/templates/citations.xlsx

	pushd "$CMIP6_HOME" || exit
	pipenv run python "$CMIP6_HOME"/lib/citations/init_xls.py --institution-id=$institution --xls-template=$xls_template
	popd || exit
}

# Invoke entry point.
_main "$1"

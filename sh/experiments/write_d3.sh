#!/usr/bin/env bash

# Main entry point.
function _main()
{
	local DIR_INPUT
	local DIR_OUTPUT
	
	declare DIR_INPUT=$CMIP6_HOME/repos/libs/esdoc-docs/cmip6/experiments/cim-documents
	declare DIR_OUTPUT=$CMIP6_HOME/repos/libs/esdoc-docs/cmip6/experiments/d3

	rm -rf "$DIR_OUTPUT"/*.*

	pipenv run python "$CMIP6_HOME"/lib/experiments/write_d3.py --input="$DIR_INPUT" --output="$DIR_OUTPUT"
}

# Invoke entry point.
_main

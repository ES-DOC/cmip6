#!/usr/bin/env bash

# Main entry point.
function _main()
{
	local INSTITUTION

	if [ "$1" ]; then
		INSTITUTION=${1}
	else
		INSTITUTION="all"
	fi

	pipenv run python "$CMIP6_HOME"/lib/parties/generate_json.py --institution-id="$INSTITUTION"
}

# Invoke entry point.
_main "$1"

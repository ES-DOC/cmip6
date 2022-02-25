#!/usr/bin/env bash

# Main entry point.
function _main()
{
        local PATH_TO_SPREADSHEET
        local DIR_IO
        local INSTITUTION

        PATH_TO_SPREADSHEET="$CMIP6_HOME"/lib/templates/performance.xlsx
        DIR_IO="$CMIP6_HOME"/repos/machines/cim-documents

        if [ "$1" ]; then
		INSTITUTION="$1"
	else
		INSTITUTION="all"
	fi

        echo "WARNING: deleting path at $DIR_IO"
        rm -rf "$DIR_IO"
	mkdir "$DIR_IO"

	pushd "$CMIP6_HOME" || exit
	pipenv run python "$CMIP6_HOME"/lib/models/generate_machine_cim.py --spreadsheet="$PATH_TO_SPREADSHEET" --io-dir="$DIR_IO" --institution-id="$INSTITUTION"
	popd || exit
}

# Invoke entry point.
_main "$1"

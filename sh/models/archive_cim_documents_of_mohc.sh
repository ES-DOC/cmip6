#!/usr/bin/env bash

# Main entry point.
function _main()
{
	local ARCHIVE_FOLDER 
	
	ARCHIVE_FOLDER=$CMIP6_HOME/repos/archives/esdoc-archive/esdoc/cmip6/spreadsheet-models
	if [ ! -d "$ARCHIVE_FOLDER" ]; then
		mkdir "$ARCHIVE_FOLDER"
	fi

	rm -rf "$ARCHIVE_FOLDER"/cmip6_mohc_*.*

	pushd "$CMIP6_HOME" || exit
	pipenv run python "$CMIP6_HOME"/lib/models/archive_cim_documents_of_mohc.py --destination="$ARCHIVE_FOLDER"
	popd || exit
}

# Invoke entry point.
_main

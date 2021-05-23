#!/usr/bin/env bash

# Main entry point.
function _main()
{
	local INSTITUTION=${1}
	local ARCHIVE_FOLDER 
	
	ARCHIVE_FOLDER=$CMIP6_HOME/repos/archives/esdoc-archive/esdoc/cmip6/spreadsheet-models
	if [ ! -d "$ARCHIVE_FOLDER" ]; then
		mkdir "$ARCHIVE_FOLDER"
	fi

	if [ "$1" ]; then
		rm -rf "$ARCHIVE_FOLDER"/cmip6_"$1"*.*
	else
		rm -rf "$ARCHIVE_FOLDER"/*.*
	fi

	pushd "$CMIP6_HOME" || exit
	pipenv run python "$CMIP6_HOME"/lib/models/archive_cim_documents.py \
		--destination="$ARCHIVE_FOLDER" \
		--institution-id="$INSTITUTION"
	popd || exit
}

# Invoke entry point.
_main "$1"

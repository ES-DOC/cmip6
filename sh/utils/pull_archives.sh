#!/usr/bin/env bash

# Main entry point.
function _main()
{
    local ARCHIVE
	local PATH_TO_REPO
	
	for ARCHIVE in "${CMIP6_ARCHIVES[@]}"
	do
        PATH_TO_REPO=$(get_path_to_repo "archives" "$ARCHIVE")
		if [ -d "$PATH_TO_REPO" ]; then
			log "GITHUB : pulling  $ARCHIVE"
			pushd "$PATH_TO_REPO" || exit
			git pull > /dev/null 2>&1
			popd || exit
		else
			log "archive repo needs to be installed: $ARCHIVE"
		fi
	done
}

# Invoke entry point.
_main

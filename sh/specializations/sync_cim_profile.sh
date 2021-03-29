#!/usr/bin/env bash

# Main entry point.
function _main()
{
	for specialization in "${CMIP6_REALM_SPECIALIZATIONS[@]}"
	do
		cp "$CMIP6_HOME"/repos/specializations/cmip6-specializations-toplevel/cim_profile.py "$CMIP6_HOME"/repos/specializations/cmip6-specializations-$specialization/generate/cim_profile.py
	done
}

# Invoke entry point.
_main

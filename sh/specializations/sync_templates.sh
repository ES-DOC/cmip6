#!/bin/bash

# Main entry point.
main()
{
	for specialization in "${CMIP6_REALM_SPECIALIZATIONS[@]}"
	do
		rm -rf $CMIP6_ROOT/cmip6-specializations-$specialization/templates
		mkdir $CMIP6_ROOT/cmip6-specializations-$specialization/templates
		cp $CMIP6_ROOT/cmip6-specializations-toplevel/templates/* $CMIP6_ROOT/cmip6-specializations-$specialization/templates
	done
}

# Invoke entry point.
main

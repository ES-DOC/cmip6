#!/bin/bash

# Main entry point.
main()
{
	declare input_dir=$ESDOC_HOME/repos/core/esdoc-docs/cmip6/experiments/cim-documents
	declare output_dir=$ESDOC_HOME/repos/core/esdoc-docs/cmip6/experiments/config

	rm -rf $output_dir/*.json

	pipenv run python $CMIP6_LIB/experiments/write_config.py --input=$input_dir --output=$output_dir
}

# Invoke entry point.
main

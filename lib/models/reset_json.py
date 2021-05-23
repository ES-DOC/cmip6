"""
.. module:: reset_json.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Resets CMIP6 model JSON documents.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import os
import shutil

from lib.utils import io_mgr
from lib.utils import vocabs



# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Resets CMIP6 model JSON files.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )

def _main(args):
    """Main entry point.

    """
    for institution in vocabs.get_institutes(args.institution_id):
        for source_id in vocabs.get_institute_sources(institution):
            folder = io_mgr.get_model_folder(institution, source_id, 'json')
            shutil.rmtree(folder)
            os.makedirs(folder)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())

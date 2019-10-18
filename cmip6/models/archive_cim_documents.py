# -*- coding: utf-8 -*-

"""
.. module:: archive_cim_documents.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Moves generated CMIP6 model CIM documets into archive.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>

"""
import argparse
import hashlib
import os
import shutil

import pyessv

from cmip6.models import utils
from cmip6.utils import vocabs
from cmip6.utils import io_mgr


# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Synchronizes CMIP6 model CIM files between institutional repos & main archive.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )
_ARGS.add_argument(
    "--destination",
    help="Folder to which CIM documents will be copied.",
    dest="dest",
    type=str
    )

# MIP era.
_MIP_ERA = "cmip6"


def _main(args):
    """Main entry point.

    """
    institutes = vocabs.get_institutes(args.institution_id)
    for i in institutes:
        for s in vocabs.get_institute_sources(i):
            _copy_files(i, s)


def _copy_files(institute, source_id):
    """Copies model files into archive.

    """
    for src in _get_cim_files(institute, source_id):
        fname = hashlib.md5(src.split("/")[-1]).hexdigest()
        dest = os.path.join(args.dest, '{}.json'.format(fname))
        shutil.copy(src, dest)


def _get_cim_files(institute, source_id):
    """Returns CIM files to be copied to documentation archive.

    """
    folder = io_mgr.get_model_folder(institute, source_id, 'cim')

    return [os.path.join(folder, i) for i in os.listdir(folder)]


# Main entry point.
if __name__ == '__main__':
    args = _ARGS.parse_args()
    if not os.path.exists(args.dest):
        raise ValueError("Destination folder is invalid")
    _main(args)

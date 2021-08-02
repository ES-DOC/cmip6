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

from lib.utils import vocabs
from lib.utils import io_mgr


# Define command line argument parser.
_ARGS = argparse.ArgumentParser("Synchronizes CMIP6 MOHC model CIM files between institutional repo & main archive.")
_ARGS.add_argument(
    "--destination",
    help="Folder to which CIM documents will be copied.",
    dest="dest",
    type=str
    )

# MIP era.
_CMIP6_MIP_ERA = "cmip6"


def _main(args):
    """Main entry point.

    """
    if not os.path.exists(args.dest):
        raise ValueError("Destination folder is invalid: {}".format(args.dest))

    institute = vocabs.get_institute("mohc")

    for _, source_id in vocabs.yield_sources(institute):
        submitted_file = _get_submitted_file(institute, source_id)
        if os.path.exists(submitted_file):
            cim_file = _get_cim_file(institute, source_id)
            shutil.copy(submitted_file, cim_file)

    for _, source_id in vocabs.yield_sources(institute):
        _copy_files_to_archive(args.dest, institute, source_id)


def _copy_files_to_archive(dest, institute, source_id):
    """Copies model files into archive.

    """
    for src_fpath in _get_cim_files(institute, source_id):
        fname = hashlib.md5(src_fpath.split("/")[-1]).hexdigest()
        dest_fpath = os.path.join(dest, '{}.json'.format(fname))
        shutil.copy(src_fpath, dest_fpath)


def _get_cim_file(institute, source_id):
    """Returns a cim file ready for archival.
    
    """
    folder = io_mgr.get_model_folder(institute, source_id, 'cim')
    fname = "cmip6_{}_{}.json".format(institute.canonical_name, source_id.canonical_name)

    return "{}/{}".format(folder, fname)


def _get_cim_files(institute, source_id):
    """Returns CIM files to be copied to documentation archive.

    """
    folder = io_mgr.get_model_folder(institute, source_id, 'cim')

    return [os.path.join(folder, i) for i in os.listdir(folder)]


def _get_submitted_file(institute, source_id):
    """Returns a submission file.
    
    """
    folder = io_mgr.get_folder((institute, 'cmip6', 'submission'))
    fname = "cmip6_{}_{}.json".format(institute.canonical_name, source_id.canonical_name)

    return "{}/{}".format(folder, fname)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())

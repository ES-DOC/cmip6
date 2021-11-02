"""
.. module:: init_performance_xls.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initialises CMIP6 per-machine per-model performance spreadsheets.

.. moduleauthor::
   Sadie Bartholomew <sadie.bartholomew@ncas.ac.uk>

"""

import argparse
import os
import shutil

from copy import copy

from openpyxl import load_workbook
from openpyxl.styles import NamedStyle, Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation

from lib.utils import io_mgr, logger, vocabs, constants


# Define command line argument parser.
_ARGS = argparse.ArgumentParser(
    "Initialises CMIP6 per-machine, per-model performance spreadsheets.")
_ARGS.add_argument(
    "--institution-id",
    help="An institution identifier",
    dest="institution_id",
    type=str,
    default="all"
    )
_ARGS.add_argument(
    "--xls-template",
    help="Path to XLS template",
    dest="xls_template",
    type=str
    )


def copy_cell(sheet, cell_to_copy_to, cell_to_copy_from):
    """Apply the value and background style of a cell to another named cell."""
    sheet[cell_to_copy_to] = sheet[cell_to_copy_from].value
    sheet[cell_to_copy_to]._style = copy(sheet[cell_to_copy_from]._style)


def set_institute_name_in_xls(institution, spreadsheet):
    """Write institute name into all relevant worksheets and their titles."""
    pass


def set_machine_name_in_xls(spreadsheet):
    """Write machine name into all relevant worksheets and their titles."""
    pass


def set_model_name_in_xls(spreadsheet, aggregate_ws_name, realm_ws_name):
    """Write model name into all relevant worksheets and their titles."""
    pass


def set_realm_name_in_xls(spreadsheet, realm_ws_name, realm_name):
    """Write realm name into all relevant worksheets and their titles."""
    pass


def create_tab_for_all_realms(spreadsheet, realm_ws_name):
    """Create one fully-formatted realm worksheet for every possible realm."""
    pass


def format_applicable_experiments(institution):
    """Pre-format applicable experiments to use in a drop-down list."""
    pass


def set_applicable_experiments_in_xls(institution, spreadsheet):
    """Write drop-down list of applicable experiments into aggregate tabs."""
    format_applicable_experiments(institution)
    pass


def _main(args):
    """Main entry point.

    """
    # Defensive programming.
    if not os.path.exists(args.xls_template):
        raise ValueError("XLS template file does not exist")

    # Take generic template ready to process with institute-specific info.
    template_name = args.xls_template
    # TODO: override for testing, remove this line at end as gets via CLI
    template_name = "templates/performance.xlsx"

    # Write out a customised template file for every institute
    for institution in vocabs.get_institutes(args.institution_id):
        institution_machines = []  # TODO SADIE
        for machine in institution_machines:
            all_models_run_on_machine = []  # TODO SADIE
            for model in all_models_run_on_machine:
                generic_template = load_workbook(filename=template_name)

                # Customise the template appropriately to the given institute:
                #   1. Set the applicable institute, machine and model names
                set_institute_name_in_xls(institution, generic_template)
                aggregate_ws_title, realm_ws_title = set_machine_name_in_xls(
                    generic_template)

                aggregate_ws_title, realm_ws_title = set_model_name_in_xls(
                    generic_template, aggregate_ws_title, realm_ws_title
                )

                #   2. Set a list of all applicable experiments as drop-down
                #      list for question 1.1.5 for the 'aggregate'
                #      performance tabs.
                set_applicable_experiments_in_xls(
                    institution, generic_template)

                #   3. Duplicate tabs and tag for every possible realm
                create_tab_for_all_realms(generic_template, realm_ws_title)

                # Close template and save customised XLS to a new XLS file
                generic_template.close()
                final_spreadsheet_name = (
                    "{}_performance_of_{}_on_{}_{}.xlsx".format(
                        constants.CMIP6_MIP_ERA, model,
                        institution.canonical_name, machine
                    )
                )
                generic_template.save(final_spreadsheet_name)

                # Place the file into the appropriate directory, ultimately
                # writing one file per machine and applicable model combination
                dest = io_mgr.get_performance_spreadsheet(
                    institution, machine, model)
                logger.log(
                    "moving xls file for {}".format(institution.raw_name))
                shutil.copy(final_spreadsheet_name, dest)


# Main entry point.
if __name__ == '__main__':
    _main(_ARGS.parse_args())

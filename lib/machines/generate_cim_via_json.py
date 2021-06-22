"""
.. module:: generate_cim_via_json.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Converts CMIP6 machine spreadsheets to CIM via intermediate JSON.

.. moduleauthor::
   Sadie Bartholomew <sadie.bartholomew@ncas.ac.uk>

"""

import json
import os
from pprint import pprint

from openpyxl import load_workbook


LABEL_COLUMN = 0  # i.e. index in A-Z of columns as tuple, so "A"
INPUT_COLUMN = 1  # i.e. "B"

EMPTY_CELL_MARKER = "NO CELL VALUE SPECIFIED"

# Usually <500, but in case of much cell copying and all exps and models listed
MAX_ROW = 600

# Is this (first one) about right? Is a guess based on seen gen'd model lists
MAX_NUMBER_MODELS_PER_INSTITUTE = 30  # TODO: replace with inst-specific value
MAX_NUMBER_MIPS = 22  # TODO: replace with inst-specific value


# Tuple keys give digits corresopnding to question labels to match to user
# inputs, e.g. (1, 1, 1) -> question "1.1.1" or "1.1.1 *", values are offsets,
# where a "SPECIAL CASE:" string value indicates extra rows may have been
# created by the user, and is to be dealt with on a case-by-case basis:
WS_QUESTIONS_TO_INPUT_CELLS_MAPPING = {
    # Identity:
    (1, 1, 1): 2,
    (1, 1, 2): 5,
    # General properties:
    (1, 2, 1): 4,
    (1, 2, 2): 2,
    (1, 2, 3): "SPECIAL CASE: 4+",
    (1, 2, 4): "SPECIAL CASE: 4+6",
    (1, 2, 5): 2,
    # Vendor information:
    (1, 3, 1): 4,
    (1, 3, 2): 2,

    # Compute pools...
    # Compute pool 1:
    (1, 4, 1, 1): 2,
    (1, 4, 1, 2): 2,
    (1, 4, 1, 3): 4,
    (1, 4, 1, 4): 2,
    (1, 4, 1, 5): 2,
    (1, 4, 1, 6): 2,
    (1, 4, 1, 7): 2,
    (1, 4, 1, 8, 1, 1): 2,
    (1, 4, 1, 8, 1, 2): 2,
    (1, 4, 1, 8, 1, 3): 4,
    (1, 4, 1, 8, 2, 1): 2,
    (1, 4, 1, 8, 2, 2): 2,
    (1, 4, 1, 8, 2, 3): 4,
    (1, 4, 1, 8, 3, 1): 2,
    (1, 4, 1, 8, 3, 2): 2,
    (1, 4, 1, 8, 3, 3): 4,
    (1, 4, 1, 9): 2,
    (1, 4, 1, 10): 2,
    (1, 4, 1, 11): 2,
    (1, 4, 1, 12): 2,
    (1, 4, 1, 13): 2,
    # Compute pool 2:  TODO, auto-gen from first Q set.
    (1, 4, 2, 1): 2,
    (1, 4, 2, 2): 2,
    (1, 4, 2, 3): 4,
    (1, 4, 2, 4): 2,
    (1, 4, 2, 5): 2,
    (1, 4, 2, 6): 2,
    (1, 4, 2, 7): 2,
    (1, 4, 2, 8, 1, 1): 2,
    (1, 4, 2, 8, 1, 2): 2,
    (1, 4, 2, 8, 1, 3): 4,
    (1, 4, 2, 8, 2, 1): 2,
    (1, 4, 2, 8, 2, 2): 2,
    (1, 4, 2, 8, 2, 3): 4,
    (1, 4, 2, 8, 3, 1): 2,
    (1, 4, 2, 8, 3, 2): 2,
    (1, 4, 2, 8, 3, 3): 4,
    (1, 4, 2, 9): 2,
    (1, 4, 2, 10): 2,
    (1, 4, 2, 11): 2,
    (1, 4, 2, 12): 2,
    (1, 4, 2, 13): 2,

    # Storage pools...
    # Storage pool 1:
    (1, 5, 1, 1): 2,
    (1, 5, 1, 2): "SPECIAL CASE: 4+",
    (1, 5, 1, 3): 2,
    (1, 5, 1, 4): 4,
    (1, 5, 1, 5): 4,
    # Storage pool 2: TODO, auto-gen from first Q set.
    (1, 5, 2, 1): 2,
    (1, 5, 2, 2): "SPECIAL CASE: 4+",
    (1, 5, 2, 3): 2,
    (1, 5, 2, 4): 4,
    (1, 5, 2, 5): 4,

    # Interconnect:
    (1, 6, 1): 2,
    (1, 6, 2): 2,
    (1, 6, 3): 2,
    (1, 6, 4): 4,
    # Benchmark performance:
    (1, 7, 1): 2,
    (1, 7, 2): 2,

    # Applicability...
    # Applicable models:
    (1, 8, 1): 2,
    # All (1, 8, 2, N) are processed in below
    # Applicable experiments:
    (1, 9, 1): 2,
    # All (1, 9, 2, N) is processed in below
}


def get_ws_questions_to_input_cells_mapping():
    input_labels = WS_QUESTIONS_TO_INPUT_CELLS_MAPPING.copy()
    # Extend the list with any potential labels for the questions:
    applicable_models_q2 = {
        (1, 8, 2, N): 1 for N in range(
            1, MAX_NUMBER_MODELS_PER_INSTITUTE)
    }
    input_labels.update(applicable_models_q2)
    applicable_experiments_q2 = {
        (1, 9, 2, N): "SPECIAL CASE: 1+" for N in range(1, MAX_NUMBER_MIPS)}
    input_labels.update(applicable_experiments_q2)

    return input_labels


def get_machine_tabs(spreadsheet):
    """TODO."""
    all_machine_tabs = []

    # Don't rely on names having 'Machine X' format as that is not certain and
    # should not be relied upon: just exclude Frontis and example tab (first
    # two tabs) and assume rest are documented machines.
    for sheet in spreadsheet:
         if sheet.title not in ("Frontis", "Example"):
             all_machine_tabs.append(sheet)

    return all_machine_tabs


def find_input_cells(spreadsheet_tab, input_labels):
    """TODO."""
    label_values = {
        ".".join(str(subsec) for subsec in label): offset for label, offset in
        input_labels.items()
    }

    # Iterate over label first so stop check on rows via break once label found
    label_to_input_cell_mapping = {}
    for label, offset in label_values.items():
        for row in spreadsheet_tab.iter_rows(
                min_row=1, max_row=MAX_ROW, max_col=2):
            label_cell_value = str(row[LABEL_COLUMN].value).strip(" *")
            if label_cell_value == label:
                # Handle special cases of input cell(s) offsets:
                if isinstance(offset, str):
                    case = offset.lstrip("SPECIAL CASE: ")
                    print("Treating a special case for the offset of:",
                          label, "with rule:", case)
                    if case.endswith("+"):
                        offsets = []
                        check_cell_at_offset = int(case.rstrip("+"))

                        # TODO: WHY IS IT INPUT_COLUMN PLUS 1: SORT IT!

                        # For N+, take all cells from N onwards until reach
                        # the first empty one, then stop:
                        while spreadsheet_tab.cell(
                                row[INPUT_COLUMN].row + check_cell_at_offset,
                                column=INPUT_COLUMN + 1
                        ).value:
                            offsets.append(check_cell_at_offset)
                            check_cell_at_offset += 1
                    else:  # not contiguous multiple input cells, other case
                        offsets = case.split("+")

                    # Institutes may, against advice, have left some
                    # experiment input cells blank to indicate no applicable
                    # experiments by MIP, so to cater for these cases, replace
                    # empty values with 'NONE'
                    if label.startswith("1.9.2.") and not offsets:
                        offsets = [1]

                    # Now add the multiple offsets as a list, then move on:
                    label_to_input_cell_mapping[label] = [
                        row[INPUT_COLUMN].row + int(offset)
                        for offset in offsets
                    ]

                    break

                # Otherwise it is a simple offset, apply it:
                input_box_row = row[INPUT_COLUMN].row + offset
                label_to_input_cell_mapping[label] = input_box_row
                break

        # Remove inapplicable numbers for MIPs and experiments:
        if not label_to_input_cell_mapping.get(label, False):
            if label.startswith("1.9.2.") or label.startswith("1.8.2."):
                # Numbers not valid in this case, too few objects, so it
                # we can just skip these...
                print("Inapplicable model or MIP number skipped:", label)


    return label_to_input_cell_mapping


def extract_inputs_at_input_cells(input_cells, spreadsheet_tab):
    """TODO."""
    values = []
    if not isinstance(input_cells, list):
        input_cells = [input_cells]
    for index, input_cell in enumerate(input_cells):
        user_input = spreadsheet_tab.cell(
            row=input_cell, column=INPUT_COLUMN + 1).value

        # Distinguish from Falsy values e.g. False and 0 as user input
        if user_input is None:
            # Use a placeholder/default that is unlikely to be specified
            # (not None, False, etc.) to avoid potential clash with any
            # user input, for keeping track of input cells left empty.
            values.append(EMPTY_CELL_MARKER)
        else:
            values.append(str(user_input))
    return values


def get_top_cell_model_or_exp_name(input_cells, spreadsheet_tab):
    """TODO.

    In all such cases, the model or experiment name is at an offset of
    zero above the first input cell, i.e. directly above it, so note the
    logic here relies on this so must be adapated to generalise further.

    """
    if not isinstance(input_cells, list):
        input_cells = [input_cells]
    lowest_row_input_cell = min(input_cells)
    name = spreadsheet_tab.cell(
        row=lowest_row_input_cell - 1, column=INPUT_COLUMN + 1).value

    return name


def convert_tab_to_dict(spreadsheet_tab):
    """TODO."""
    all_input_cells = find_input_cells(
        spreadsheet_tab, get_ws_questions_to_input_cells_mapping())

    final_dict = {}
    for label, input_cell_or_cells in all_input_cells.items():
        if not isinstance(input_cell_or_cells, list):
            user_input = spreadsheet_tab.cell(
                row=input_cell_or_cells, column=INPUT_COLUMN + 1).value

            # Distinguish from Falsy values e.g. False and "None" as user input
            if user_input is None:
                # Use a placeholder/default that is unlikely to be specified
                # (not None, False, etc.) to avoid potential clash with any
                # user input, for keeping track of input cells left empty.
                final_dict[label] = EMPTY_CELL_MARKER
            else:  # else store the value, which may (rarely) be string "None"!
                # For cases where questions are populated based on institute
                # specific values (e.g. applicable models and exps questions),
                # also note these values for validation
                if label.startswith("1.8.2."):
                    name = get_top_cell_model_or_exp_name(
                        input_cell_or_cells, spreadsheet_tab)
                    final_dict[label] = {name: str(user_input)}
                else:
                    try:
                        final_dict[label] = str(user_input)
                    except:
                        # Python 2 only unicode-escape
                        print(
                            "WARNING: Python 2 only unicode issue with:",
                            label
                        )
                        final_dict[label] = user_input
        elif label.startswith("1.9.2."):
            if not spreadsheet_tab.cell(
                row=input_cell_or_cells[0], column=INPUT_COLUMN + 1).value:
                # Institutes may, against advice, have left some
                # experiment input cells blank to indicate no applicable
                # experiments by MIP, so to cater for these cases, replace
                # empty values with 'NONE'
                final_dict[label] = "NONE"
            else:
                name = get_top_cell_model_or_exp_name(
                    input_cell_or_cells, spreadsheet_tab)  # TODO issue here
                final_dict[label] = {name: extract_inputs_at_input_cells(
                    input_cell_or_cells, spreadsheet_tab)}
        else:
            final_dict[label] = extract_inputs_at_input_cells(
                input_cell_or_cells, spreadsheet_tab)

    return final_dict


def convert_intermediate_dict_to_cim(json):
    """TODO."""
    std_json = None
    return std_json


def generate_cim_outputs(machines_spreadsheet):
    """TODO."""
    machine_cim_outputs = []

    tabs = get_machine_tabs(machines_spreadsheet)
    for machine_tab in tabs:
        print("CONVERTING TAB:")
        pprint(machine_tab)
        dict_out = convert_tab_to_dict(machine_tab)
        print("INTERMEDIATE DICT IS:")
        pprint(dict_out)
        cim = convert_intermediate_dict_to_cim(dict_out)
        print("CIM IS:")
        pprint(cim)
        machine_cim_outputs.append(cim)

    return machine_cim_outputs


# Main entry point.
if __name__ == '__main__':
    # Locate and open template
    spreadsheet_path = os.path.join(
        "test-machine-sheets", "ipsl_real_submission.xlsx"
    )  # TODO, TEMP: for testing
    open_spreadsheet = load_workbook(filename=spreadsheet_path)

    # Extract CIM
    cim_outputs = generate_cim_outputs(open_spreadsheet)

    # Close template
    open_spreadsheet.close()

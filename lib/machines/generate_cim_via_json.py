"""
.. module:: generate_cim_via_json.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initialises CMIP6 machines spreadsheets.

.. moduleauthor::
   Sadie Bartholomew <sadie.bartholomew@ncas.ac.uk>

"""

import json
import pprint

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
input_labels = {
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

# Extend the list with any potential labels for the questions:
applicable_models_q2 = {
    (1, 8, 2, N): 1 for N in range(
        1, MAX_NUMBER_MODELS_PER_INSTITUTE)
}
applicable_experiments_q2 = {
    (1, 9, 2, N): "SPECIAL CASE: 1+" for N in range(1, MAX_NUMBER_MIPS)}
input_labels.update({**applicable_models_q2, **applicable_experiments_q2})


def get_machine_tabs(spreadsheet):
    """TODO."""
    all_machine_tabs = []

    # Don't rely on names having 'Machine X' format as that is not certain and
    # should not be relied upon: just exclude Frontis and example tab (first
    # two tabs) and assume rest are documented machines.
    for sheet in spreadsheet:
         if sheet.title not in ("Frontis", "Example"):
             all_machine_tabs.append(sheet)

    # TODO, TEMP: remove this bodge to use example tab as an easy test
    return [spreadsheet["Example"]]


def find_input_cells(spreadsheet_tab):
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

        # Remove inapplicable MIPs and experiments:
        if not label_to_input_cell_mapping.get(label, False):
            if label.startswith("1.9.2.") or label.startswith("1.8.2."):
                # Skip these special cases for now
                # TODO: sort this later
                print("Inapplicable model or MIP question skipped:", label)

    return label_to_input_cell_mapping


def convert_tab_to_json(spreadsheet_tab):
    """TODO."""
    all_input_cells = find_input_cells(spreadsheet_tab)

    final_json = {}
    for label, input_cell_or_cells in all_input_cells.items():
        if not isinstance(input_cell_or_cells, list):
            user_input = spreadsheet_tab.cell(
                row=input_cell_or_cells, column=INPUT_COLUMN + 1).value

            # Distinguish from Falsy values e.g. False and "None" as user input
            if user_input is None:
                # Use a placeholder/default that is unlikely to be specified
                # (not None, False, etc.) to avoid potential clash with any
                # user input, for keeping track of input cells left empty.
                final_json[label] = EMPTY_CELL_MARKER
            else:  # else store the value, which may (rarely) be string "None"!
                final_json[label] = str(user_input)
        else:
            values = []
            for index, input_cell in enumerate(input_cell_or_cells):
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
            final_json[label] = values

    return json.dumps(final_json, indent=4)


def convert_json_to_cim(json):
    """TODO."""
    final_cim = None
    return final_cim


def generate_cim(machines_spreadsheet):
    """TODO."""
    cim_outputs = []

    tabs = get_machine_tabs(machines_spreadsheet)
    for machine_tab in tabs:
        print("CONVERTING TAB:", machine_tab)
        json = convert_tab_to_json(machine_tab)
        print("JSON IS:", json)
        cim = convert_json_to_cim(json)
        print("CIM IS:")
        pprint.pprint(cim)
        cim_outputs.append(cim)

    return cim_outputs


# Main entry point.
if __name__ == '__main__':
    # Locate and open template
    spreadsheet_path = "templates/machines.xlsx"  # TODO, TEMP: for testing
    open_spreadsheet = load_workbook(filename=spreadsheet_path)

    # Extract CIM
    cim_outputs = generate_cim(open_spreadsheet)

    # Close template
    open_spreadsheet.close()

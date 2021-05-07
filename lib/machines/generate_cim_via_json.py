"""
.. module:: generate_cim_via_json.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initialises CMIP6 machines spreadsheets.

.. moduleauthor::
   Sadie Bartholomew <sadie.bartholomew@ncas.ac.uk>

"""

import json

from openpyxl import load_workbook


LABEL_COLUMN = 0  # i.e. index in A-Z of columns as tuple, so "A"
INPUT_COLUMN = 1  # i.e. "B"

# Usually <500, but in case of much cell copying and all exps and models listed
MAX_ROW = 600

# Is this (first one) about right? Is a guess based on seen gen'd model lists
MAX_NUMBER_MODELS_PER_INSTITUTE = 30  # TODO: replace with inst-specific value
MAX_NUMBER_MIPS = 22  # TODO: replace with inst-specific value


# Tuples give digits corresopnding to question labels to match to user inputs,
# e.g. (1, 1, 1) -> question "1.1.1" or "1.1.1 *"
input_labels = [
    # Identity:
    (1, 1, 1),
    (1, 1, 2),
    # General properties:
    (1, 2, 1),
    (1, 2, 2),
    (1, 2, 3),
    (1, 2, 4),
    (1, 2, 5),
    # Vendor information:
    (1, 3, 1),
    (1, 3, 2),

    # Compute pools...
    # Compute pool 1:
    (1, 4, 1, 1),
    (1, 4, 1, 2),
    (1, 4, 1, 3),
    (1, 4, 1, 4),
    (1, 4, 1, 5),
    (1, 4, 1, 6),
    (1, 4, 1, 7),
    (1, 4, 1, 8, 1, 1),
    (1, 4, 1, 8, 1, 2),
    (1, 4, 1, 8, 1, 3),
    (1, 4, 1, 8, 2, 1),
    (1, 4, 1, 8, 2, 2),
    (1, 4, 1, 8, 2, 3),
    (1, 4, 1, 8, 3, 1),
    (1, 4, 1, 8, 3, 2),
    (1, 4, 1, 8, 3, 3),
    (1, 4, 1, 9),
    (1, 4, 1, 10),
    (1, 4, 1, 11),
    (1, 4, 1, 12),
    (1, 4, 1, 13),
    # Compute pool 2:
    (1, 4, 2, 1),
    (1, 4, 2, 2),
    (1, 4, 2, 3),
    (1, 4, 2, 4),
    (1, 4, 2, 5),
    (1, 4, 2, 6),
    (1, 4, 2, 7),
    (1, 4, 2, 8, 1, 1),
    (1, 4, 2, 8, 1, 2),
    (1, 4, 2, 8, 1, 3),
    (1, 4, 2, 8, 2, 1),
    (1, 4, 2, 8, 2, 2),
    (1, 4, 2, 8, 2, 3),
    (1, 4, 2, 8, 3, 1),
    (1, 4, 2, 8, 3, 2),
    (1, 4, 2, 8, 3, 3),
    (1, 4, 2, 9),
    (1, 4, 2, 10),
    (1, 4, 2, 11),
    (1, 4, 2, 12),
    (1, 4, 2, 13),

    # Storage pools...
    # Storage pool 1:
    (1, 5, 1, 1),
    (1, 5, 1, 2),
    (1, 5, 1, 3),
    (1, 5, 1, 4),
    (1, 5, 1, 5),
    # Storage pool 2:
    (1, 5, 2, 1),
    (1, 5, 2, 2),
    (1, 5, 2, 3),
    (1, 5, 2, 4),
    (1, 5, 2, 5),

    # Interconnect:
    (1, 6, 1),
    (1, 6, 2),
    (1, 6, 3),
    (1, 6, 4),
    # Benchmark performance:
    (1, 7, 1),
    (1, 7, 2),

    # Applicability...
    # Applicable models:
    (1, 8, 1),
    # All (1, 8, 2, N) are processed in below
    # Applicable experiments:
    (1, 9, 1),
    # All (1, 9, 2, N) is processed in below
]

# Extend the list with any potential labels for the questions:
applicable_models_q2 = [
    (1, 8, 2, N) for N in range(1, MAX_NUMBER_MODELS_PER_INSTITUTE)]
applicable_experiments_q2 = [(1, 9, 2, N) for N in range(1, MAX_NUMBER_MIPS)]
input_labels.extend(applicable_models_q2 + applicable_experiments_q2)


def get_machine_tabs(spreadsheet):
    """TODO."""
    all_machine_tabs = []

    # Don't rely on names having 'Machine X' format as that is not certain and
    # should not be relied upon: just exclude Frontis and example tab (first
    # two tabs) and assume rest are documented machines.
    for sheet in spreadsheet:
         if sheet.title not in ("Frontis", "Example"):
             all_machine_tabs.append(sheet)

    # print(all_machine_tabs)
    #return all_machine_tabs

    # TODO, TEMP: remove this bodge to use example tab as an easy test
    return [spreadsheet["Example"]]


def find_input_cells(spreadsheet_tab):
    """TODO."""
    label_values = [
        ".".join(str(subsec) for subsec in label) for label in input_labels]
    label_to_input_cell_mapping = {}

    # Iterate over label first so stop check on rows via break once label found
    for label in label_values:
        for row in spreadsheet_tab.iter_rows(
                min_row=1, max_row=MAX_ROW, max_col=2):
            label_cell_value = str(row[LABEL_COLUMN].value).strip(" *")
            if label_cell_value == label:
                label_to_input_cell_mapping[label] = row[INPUT_COLUMN]
                break

        # Remove inapplicable MIPs and experiments:
        if not label_to_input_cell_mapping.get(label, False):
            if label.startswith("1.9.2.") or label.startswith("1.8.2."):
                # Skip these cases
                print("Inapplicable model or MIP question skipped:", label)
            else:
                # Use a placeholder/default that is unlikely to be specified
                # (not None, False, etc.) to avoid potential clash with any
                # user input for keeping track of input cells left empty.
                label_to_input_cell_mapping[label] = "EMPTY"


    # TODO: need to apply offsets to get actual input cells (often one or
    # two cells down) from the cell adjacent to the sub-section label

    return label_to_input_cell_mapping


def convert_tab_to_json(spreadsheet_tab):
    """TODO."""
    print(find_input_cells(spreadsheet_tab))

    final_json = json.dumps({})
    return final_json


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
        print("CIM IS:", cim)
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

    print(cim_outputs)

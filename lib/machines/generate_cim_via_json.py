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

import pyesdoc
from pyesdoc.ontologies.cim import v2 as cim


PRINT_WARNINGS = False

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

INSTITUTE = "an institute"  # TODO: hook up to CLI
KWARGS = {
    "project": "CMIP6",
    "source": "spreadsheet",
    "version": 1,
    "institute": INSTITUTE
}

QUESTIONS_TO_CIM_MAPPING = {
    # Identity:
    (1, 1, 1): ("name",),
    (1, 1, 2): ("partition", "name"),
    # General properties:
    (1, 2, 1): ("institution",),
    (1, 2, 2): ("description",),
    (1, 2, 3): ("online_documentation",),
    (1, 2, 4): ("when_used",),
    ### (1, 2, 5): ("operating_system",),  # TODO CIM V2.0 -> V2.2
    # Vendor information:
    (1, 3, 1): ("vendor",),
    (1, 3, 2): ("model_number",),
    # Compute pools...
    # Compute pool 1:
    (1, 4, 1, 1): ("compute_pools", "name"),
    (1, 4, 1, 2): ("compute_pools", "description"),
    ### (1, 4, 1, 3): ("compute_pools", "vendor"),  # TODO CIM V2.0 -> V2.2
    (1, 4, 1, 4): ("compute_pools", "model_number"),
    (1, 4, 1, 5): ("compute_pools", "number_of_nodes"),
    (1, 4, 1, 6): ("compute_pools", "memory_per_node"),
    (1, 4, 1, 7): ("compute_pools", "compute_cores_per_node"),
    # TODO CIM V2.0 -> V2.2, NIC component:
    ### (1, 4, 1, 8, 1, 1): ("compute_pools", "nic", "name"),
    ### (1, 4, 1, 8, 1, 2): ("compute_pools", "nic", "bandwidth"),
    ### (1, 4, 1, 8, 1, 3): ("compute_pools", "nic", "vendor"),
    ### (1, 4, 1, 8, 2, 1): ("compute_pools", "nic", "name"),
    ### (1, 4, 1, 8, 2, 2): ("compute_pools", "nic", "bandwidth"),
    ### (1, 4, 1, 8, 2, 3): ("compute_pools", "nic", "vendor"),
    ### (1, 4, 1, 8, 3, 1): ("compute_pools", "nic", "name"),
    ### (1, 4, 1, 8, 3, 2): ("compute_pools", "nic", "bandwidth"),
    ### (1, 4, 1, 8, 3, 3): ("compute_pools", "nic", "vendor"),
    (1, 4, 1, 9): ("compute_pools", "accelerators_per_node"),
    (1, 4, 1, 10): ("compute_pools", "accelerator_type"),
    (1, 4, 1, 11): ("compute_pools", "cpu_type"),
    (1, 4, 1, 12): ("compute_pools", "clock_speed"),
    (1, 4, 1, 13): ("compute_pools", "clock_cycle_concurrency"),
    # Compute pool 2:
    (1, 4, 2, 1): ("compute_pools", "name"),
    (1, 4, 2, 2): ("compute_pools", "description"),
    ###(1, 4, 2, 3): ("compute_pools", "vendor"),  # TODO CIM V2.0 -> V2.2
    (1, 4, 2, 4): ("compute_pools", "model_number"),
    (1, 4, 2, 5): ("compute_pools", "number_of_nodes"),
    (1, 4, 2, 6): ("compute_pools", "memory_per_node"),
    (1, 4, 2, 7): ("compute_pools", "compute_cores_per_node"),
    # TODO CIM V2.0 -> V2.2, NIC component:
    ### (1, 4, 2, 8, 1, 1): ("compute_pools", "nic", "name"),
    ### (1, 4, 2, 8, 1, 2): ("compute_pools", "nic", "bandwidth"),
    ### (1, 4, 2, 8, 1, 3): ("compute_pools", "nic", "vendor"),
    ### (1, 4, 2, 8, 2, 1): ("compute_pools", "nic", "name"),
    ### (1, 4, 2, 8, 2, 2): ("compute_pools", "nic", "bandwidth"),
    ### (1, 4, 2, 8, 2, 3): ("compute_pools", "nic", "vendor"),
    ### (1, 4, 2, 8, 3, 1): ("compute_pools", "nic", "name"),
    ### (1, 4, 2, 8, 3, 2): ("compute_pools", "nic", "bandwidth"),
    ### (1, 4, 2, 8, 3, 3): ("compute_pools", "nic", "vendor"),
    (1, 4, 2, 9): ("compute_pools", "accelerators_per_node"),
    (1, 4, 2, 10): ("compute_pools", "accelerator_type"),
    (1, 4, 2, 11): ("compute_pools", "cpu_type"),
    (1, 4, 2, 12): ("compute_pools", "clock_speed"),
    (1, 4, 2, 13): ("compute_pools", "clock_cycle_concurrency"),
    # Storage pools...
    # Storage pool 1:
    (1, 5, 1, 1): ("storage_pools", "name"),
    # TODO CIM V2.0 -> V2.2:
    ### (1, 5, 1, 2): ("storage_pools", "file_system_sizes"),
    (1, 5, 1, 3): ("storage_pools", "description"),
    (1, 5, 1, 4): ("storage_pools", "type"),
    (1, 5, 1, 5): ("storage_pools", "vendor"),
    # Storage pool 2:
    (1, 5, 2, 1): ("storage_pools", "name"),
    # TODO CIM V2.0 -> V2.2:
    ### (1, 5, 2, 2): ("storage_pools", "file_system_sizes"),
    (1, 5, 2, 3): ("storage_pools", "description"),
    (1, 5, 2, 4): ("storage_pools", "type"),
    (1, 5, 2, 5): ("storage_pools", "vendor"),
    # Interconnect:
    # TODO CIM V2.0 -> V2.2 *and* third level:
    ### (1, 6, 1): ("compute_pools", "interconnect", "name"),
    ### (1, 6, 2): ("compute_pools", "interconnect", "topology"),
    ### (1, 6, 3): ("compute_pools", "interconnect", "description"),
    ### (1, 6, 4): ("compute_pools", "interconnect", "vendor"),
    # Benchmark performance:
    # TODO CIM V2.0 -> V2.2:
    ### (1, 7, 1): ("peak_performance",),
    ### (1, 7, 2): ("linpack_performance",),
}


def get_ws_questions_to_input_cells_mapping():
    """TODO."""
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
                    if PRINT_WARNINGS:
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
                if PRINT_WARNINGS:
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
                        if PRINT_WARNINGS:
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


def init_machine_cim():
    """TODO."""
    # Define the overall document which will be populated below
    machine_cim = pyesdoc.create(cim.Machine, **KWARGS)

    # First-level properties, being their own platform classes
    partition_cim = pyesdoc.create(cim.Partition, **KWARGS)

    # Create two compute pools and storage pools, since the machine
    # spreadsheet assumption was that there would be no more than two of
    # either of these. If only one of either is described, the other is
    # removed later when it becomes known to not be applicable.
    compute_pools_cim_1 = pyesdoc.create(cim.ComputePool, **KWARGS)
    compute_pools_cim_2 = pyesdoc.create(cim.ComputePool, **KWARGS)
    storage_pools_cim_1 = pyesdoc.create(cim.StoragePool, **KWARGS)
    storage_pools_cim_2 = pyesdoc.create(cim.StoragePool, **KWARGS)

    # Connect the first-level properties to the top-level machine document
    machine_cim.partition = partition_cim
    machine_cim.compute_pools = [compute_pools_cim_1, compute_pools_cim_2]
    machine_cim.storage_pools = [storage_pools_cim_1, storage_pools_cim_2]
    return machine_cim


def map_question_inputs_to_machine_cim(inputs_by_question_number_json):
    """TODO."""
    # 1. Filter out inputs where no value was specified, by marker
    submitted_inputs = {
        q_no: val for q_no, val in inputs_by_question_number_json.items() if
        val != EMPTY_CELL_MARKER
    }

    # 2. Inititate machine CIM document
    machine_doc = init_machine_cim()

    # 3. Chnage tuple of int question numebr labels to dot-delimited string
    questions_to_cim_mapping_str = {
        ".".join([str(int) for int in q_no]): val for q_no, val in
        QUESTIONS_TO_CIM_MAPPING.items()
    }

    # 4. Match submitted questions to their corresponding machine CIM
    #    components and set them accordingly on the document object
    for q_no, q_answer in submitted_inputs.items():
        if q_no in questions_to_cim_mapping_str:
            corr_cim_comp = questions_to_cim_mapping_str[q_no]
            level = len(corr_cim_comp)

            # a) Top level comps
            if level == 1:
                setattr(machine_doc, corr_cim_comp[0], q_answer)
            elif level == 2:  # b) second-level comps e.g. storage pool
                level_1_comp, level_2_comp = corr_cim_comp

                # Special cases where need to set on one of two list values
                if level_1_comp in ("compute_pools", "storage_pools"):
                    # Determine if this is the first or second pool, as can
                    # indicated by the third value in the question number
                    # (1 -> first => Python index 0, etc.)
                    pool_index = int(str(q_no.split(".")[2])) - 1
                    # Set the value on the correct pool in the length-two list
                    setattr(
                        getattr(machine_doc, level_1_comp)[pool_index],
                        level_2_comp, q_answer
                    )
                else:
                    setattr(
                        getattr(machine_doc, level_1_comp),
                        level_2_comp, q_answer
                    )
            else:
                ValueError(
                    "Machine CIM should not be more than two levels deep."
                )

    # 4. Return completed machine CIM document - passed through anyway...
    return machine_doc


def convert_intermediate_dict_to_cim(intermediate_dict):
    """TODO."""
    return map_question_inputs_to_machine_cim(intermediate_dict)


def generate_cim_outputs(machines_spreadsheet):
    """TODO."""
    machine_cim_outputs = []

    tabs = get_machine_tabs(machines_spreadsheet)
    for machine_tab in tabs:
        ###print("CONVERTING TAB:")
        ###pprint(machine_tab)
        dict_out = convert_tab_to_dict(machine_tab)
        print("INTERMEDIATE DICT IS:")
        pprint(dict_out)

        # Print applicable models to test
        models = get_applicable_models(dict_out)
        print("APPLICABLE MODELS ARE:", models)

        # Print applicable experiments to test
        exps = get_applicable_experiments(dict_out)
        print("APPLICABLE EXPS ARE:", exps)
        
        cim = convert_intermediate_dict_to_cim(dict_out)
        print("CIM IS:")
        pprint(cim)

        """
        print("\n*** INSPECT MACHINE CIM DOC TO CHECK IT LOOKS OK ***\n")
        pprint(cim.__dict__)
        pprint(cim.partition.__dict__)
        pprint(cim.compute_pools[0].__dict__)
        pprint(cim.compute_pools[1].__dict__)
        pprint(cim.storage_pools[0].__dict__)
        pprint(cim.storage_pools[1].__dict__)
        """

        machine_cim_outputs.append(cim)

    return machine_cim_outputs


def get_applicable_models(intermediate_dict):
    """TODO."""
    model_appl_answers = {
        q_no: q_ans for (q_no, q_ans) in intermediate_dict.items()
        if q_no.startswith("1.8")
    }
    all_applicable = model_appl_answers.pop("1.8.1")
    models_with_appl = model_appl_answers.values()

    if all_applicable == "ALL":
        # Take all listed models, so take all model keys regardless of value
        applicable_models = models_with_appl.keys()
    elif all_applicable == "SOME":
        # In this case must filter out ones specified as not being applicable
        applicable_models = [
            appl.keys()[0] for appl in models_with_appl if
            appl.values()[0] == "YES"
        ]
    else:
        raise ValueError(
            "Invalid input to enum. with 'ALL' or 'SOME' option only.")

    return applicable_models


def get_applicable_experiments(intermediate_dict):
    """TODO."""
    exp_appl_answers = {
        q_no: q_ans for (q_no, q_ans) in intermediate_dict.items()
        if q_no.startswith("1.9")
    }
    all_applicable = exp_appl_answers.pop("1.9.1")
    exp_with_appl = exp_appl_answers.values()

    if all_applicable == "ALL":
        # TODO, requires func from machine spreadsheet processing...
        pass
    elif all_applicable == "SOME":
        # In this case must filter out ones specified as not being applicable
        applicable_exps = {
            appl.keys()[0]: appl.values()[0] for appl in exp_with_appl if
            appl.values()[0] != ["NONE"]
        }
        # TODO for rigour, add test to check for any weird inputs, e.g. None
        # in a list with named experiments...
    else:
        raise ValueError(
            "Invalid input to enum. with 'ALL' or 'SOME' option only.")

    return applicable_exps


# Main entry point.
if __name__ == '__main__':
    # Locate and open template
    spreadsheet_path = os.path.join(
        "test-machine-sheets", "ipsl_real_submission.xlsx"
    )  # TODO, TEMP: for testing
    open_spreadsheet = load_workbook(filename=spreadsheet_path)

    # Extract CIM
    cim_outputs = generate_cim_outputs(open_spreadsheet)

    # Test serlialisation...
    for cim_out in cim_outputs:
        j = pyesdoc.encode(cim_out, "json")
        ###print("FINAL OUTPUT IS")
        ###pprint(j)
        assert json.loads(j)
        # TODO decoding broken below...
        ### assert isinstance(pyesdoc.decode(j, "json"), cim.Machine)

        x = pyesdoc.encode(cim_out, "xml")
        # TODO, fix XML decoding errors like:
        # "Scalar decoding error 2.7 GHz <type 'float'>"
        assert isinstance(pyesdoc.decode(x, "xml"), cim.Machine)

    # Close template
    open_spreadsheet.close()

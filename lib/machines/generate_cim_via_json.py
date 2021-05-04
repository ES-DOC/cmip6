"""
.. module:: generate_cim_via_json.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Initialises CMIP6 machines spreadsheets.

.. moduleauthor::
   Sadie Bartholomew <sadie.bartholomew@ncas.ac.uk>

"""


def get_machine_tabs(spreadsheet):
    """TODO."""
    all_tabs = []
    return all_tabs


def convert_tab_to_json(spreadsheet_tab):
    """TODO."""
    final_json = None
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
        json = convert_spreadsheet_to_json(machine_tab)
        cim = convert_json_to_cim(json)
        cim_outputs.append(cim)

    return cim_outputs


# Main entry point.
if __name__ == '__main__':
    template_name = "templates/machines.xlsx"
    cim_outputs = generate_cim(template_name)
    print(cim_outputs)

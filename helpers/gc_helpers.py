"""
This module contains the helpers functions for reading genetic code table
information from json file.
"""

import json

# Read the list of genetic codes and associated files in a dictionary.
with open("gc_files/gc_file_directory") as gc_directory:
    gc_file_associations = json.load(gc_directory)


def codon2AA(codon, gc=1):
    """
    This functions returns the respective amino acid for the given codon
    :param codon: Codon (string) e.g. AAA
    :param gc: genetic code (integer) default = 1
    :return:
    """
    try:
        if str(gc) not in gc_file_associations.keys:
            # No entry for the required genetic code
            return None
        # Read the file
        with open(gc_file_associations.get(str(gc))) as gc_file:
            gc_data = json.load(gc_file)

        for key in gc_data.keys:
            aa_data = gc_data.get(key)
            if codon in aa_data['codon']:
                # found the codon, return AA key.
                return key
        # Could not find this codon in any AA's data.
        return None
    except Exception:
        return None


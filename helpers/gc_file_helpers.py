"""
This module contains the helpers functions for reading genetic code table
information from json file.
"""

import json

# Read the list of genetic codes and associated files in a dictionary.
with open("gc_files/gc_file_associations.json") as gc_directory:
    gc_file_associations = json.load(gc_directory)


def codon_to_aa(codon, gc=1):
    """
    This functions returns 3 letter notation e.g. 'ala' for amino acid
    respective to given codon.
    :param codon: Codon (string) e.g. AAA
    :param gc: genetic code (Integer) default=1 i.e. standard_genetic_code
    :return:
    """
    try:
        if str(gc) not in gc_file_associations.keys():
            # No entry for the required genetic code
            return None
        # Read the file
        with open(gc_file_associations.get(str(gc))) as gc_file:
            gc_data = json.load(gc_file)

        for key in gc_data.keys():
            aa_data = gc_data.get(key)
            if codon in aa_data["codons"]:
                # found the codon, return AA key.
                return key
        # Could not find this codon in any AA's data.
        return None
    except Exception:
        return None


def aa_to_codon(aa, gc=1):
    """
    This function returns the list of codons for given amino acid according
    to respective genetic code table.
    :param aa: amino acid notation/ name (String) e.g. Full name e.g. Alanine or
    3-letter notation e.g. Ala or single letter notation e.g. A
    :param gc: genetic code (Integer) default=1 i.e. standard_genetic_code
    :return:
    """
    try:
        if str(gc) not in gc_file_associations.keys():
            # No entry for the required genetic code
            return None
        # Read the file for genetic code table information
        with open(gc_file_associations.get(str(gc))) as gc_file:
            gc_data = json.load(gc_file)

        # if notation is given
        if len(aa) == 3:
            if aa.lower() in gc_data.keys():
                return gc_data.get(aa.lower())["codons"]
        # lookup for fullname or notation
        for key in gc_data.keys():
            aa_data = gc_data.get(key)
            if aa_data["name"].lower() == aa.lower() or \
                aa_data["symbol"].lower() == aa.lower():
                return aa_data["codons"]

        # If nothing is found, return None
        return None

    except Exception:
        return None


def get_aa_using_name(aa, gc=1):
    """
    This function returns a dictionary object containing
    :param aa: amino acid notation/ name (String) e.g. Full name e.g. Alanine or
    3-letter notation e.g. Ala or single letter notation e.g. A
    :param gc: genetic code (Integer) default=1 i.e. standard_genetic_code
    :return:
    """
    try:
        if str(gc) not in gc_file_associations.keys():
            # No entry for the required genetic code
            return None
        # Read the file for genetic code table information
        with open(gc_file_associations.get(str(gc))) as gc_file:
            gc_data = json.load(gc_file)

        # if notation is given
        if len(aa) == 3:
            if aa.lower() in gc_data.keys():
                return gc_data.get(aa.lower())
        # lookup for fullname or notation
        for key in gc_data.keys():
            aa_data = gc_data.get(key)
            if aa_data["name"].lower() == aa.lower() or \
                aa_data["symbol"].lower() == aa.lower():
                return aa_data

        # If nothing is found, return None
        return None

    except Exception:
        return None


def get_aa_using_codon(codon, gc=1):
    """
    This functions returns dictionary object containing data for respective
    amino acid for the given codon.
    :param codon: Codon (string) e.g. AAA
    :param gc: genetic code (Integer) default=1 i.e. standard_genetic_code
    :return:
    """
    try:
        if str(gc) not in gc_file_associations.keys():
            # No entry for the required genetic code
            return None
        # Read the file
        with open(gc_file_associations.get(str(gc))) as gc_file:
            gc_data = json.load(gc_file)

        for key in gc_data.keys():
            aa_data = gc_data.get(key)
            if codon in aa_data["codons"]:
                # found the codon, return AA key.
                return aa_data
        # Could not find this codon in any AA's data.
        return None
    except Exception:
        return None


def get_synonymous_codons(codon, gc=1):
    """
    This functions returns list object containing synonymous codons for given
    codon.
    :param codon: Codon (string) e.g. AAA
    :param gc: genetic code (Integer) default=1 i.e. standard_genetic_code
    :return:
    """
    try:
        if str(gc) not in gc_file_associations.keys():
            # No entry for the required genetic code
            return None
        # Read the file
        with open(gc_file_associations.get(str(gc))) as gc_file:
            gc_data = json.load(gc_file)

        for key in gc_data.keys():
            aa_data = gc_data.get(key)
            if codon in aa_data["codons"]:
                # found the codon, return AA key.
                return aa_data["codons"]
        # Could not find this codon in any AA's data.
        return None
    except Exception:
        return None

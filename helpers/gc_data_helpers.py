"""
This module contains the helpers functions for reading genetic code
information from json/dictionary object.
"""

import json

# Read the list of genetic codes and associated files in a dictionary.
with open("gc_files/gc_file_associations.json") as gc_directory:
    gc_file_associations = json.load(gc_directory)


def get_gc_table(filename=None, path=None):
    """
    This function read the gc table from a json file and returns it to as a
    dictionary.
    :param filename: name of the file  gc table file. default folder to look
    into = gc_files/.
    :param path: fully qualified path for gc table json file. if both name and
    path are given, path is preferred for looking up file.
    :return:
    """
    gc_table_data = None
    if path is not None:
        try:
            with open(path) as gc_file:
                gc_table_data = json.load(gc_file)
                if gc_table_data is not None:
                    return gc_table_data
        except:
            pass
    elif filename is not None:
        try:
            with open('gc_files/' + filename) as gc_file:
                gc_table_data = json.load(gc_file)
                if gc_table_data is not None:
                    return gc_table_data
        except:
            return None
    else:
        # Invalid data provided. both paramters are none
        return None


def codon_to_aa_gct(gct=None, codon=None):
    """
    This functions returns 3 letter notation e.g. 'ala' for amino acid
    respective to given codon.
    :param gct: dictionary object containing gc table data.
    :param codon: Codon (string) e.g. AAA
    :return:
    """
    try:
        if gct is None or codon is None:
            # invalid set of inputs provided
            print("one is none")
            return None

        for key in gct.keys():
            aa_data = gct.get(key)
            if codon.upper() in aa_data["codons"]:
                # found the codon, return AA key.
                return key
        # Could not find this codon in any AA's data.
        return None
    except Exception as e:
        print(e)
        return None


def aa_to_codon_gct(gct=None, aa=None):
    """
    This function returns the list of codons for given amino acid according
    to respective genetic code table.
    :param gct: dictionary object containing gc table data.
    :param aa: amino acid notation/ name (String) e.g. Full name e.g. Alanine or
    3-letter notation e.g. Ala or single letter notation e.g. A
    :return:
    """
    try:
        if gct is None or aa is None:
            # Invalid set of inputs provided
            return None

        # if notation is given
        if len(aa) == 3:
            if aa.lower() in gct.keys():
                return gct.get(aa.lower())["codons"]
        # lookup for fullname or notation
        for key in gct.keys():
            aa_data = gct.get(key)
            if aa_data["name"].lower() == aa.lower() or \
                            aa_data["symbol"].lower() == aa.lower():
                return aa_data["codons"]

        # If nothing is found, return None
        return None

    except Exception:
        return None


def get_aa_using_name_gct(gct=None, aa=None):
    """
    This function returns a dictionary object containing
    :param gct: dictionary object containing gc table data.
    :param aa: amino acid notation/ name (String) e.g. Full name e.g. Alanine or
    3-letter notation e.g. Ala or single letter notation e.g. A
    :return:
    """
    try:
        if gct is None or aa is None:
            # Invalid set of inputs provided
            return None
        # if notation is given
        if len(aa) == 3:
            if aa.lower() in gct.keys():
                return gct.get(aa.lower())
        # lookup for fullname or notation
        for key in gct.keys():
            aa_data = gct.get(key)
            if aa_data["name"].lower() == aa.lower() or \
                            aa_data["symbol"].lower() == aa.lower():
                return aa_data

        # If nothing is found, return None
        return None

    except Exception:
        return None


def get_aa_using_codon_gct(gct=None, codon=None):
    """
    This functions returns dictionary object containing data for respective
    amino acid for the given codon.
    :param gct: dictionary object containing gc table data.
    :param codon: Codon (string) e.g. AAA
    :return:
    """
    try:
        if gct is None or codon is None:
            # Invalid set of inputs provided
            return None
        for key in gct.keys():
            aa_data = gct.get(key)
            if codon in aa_data["codons"]:
                # found the codon, return AA key.
                return aa_data
        # Could not find this codon in any AA's data.
        return None
    except Exception:
        return None


def get_synonymous_codons_gct(gct=None, codon=None):
    """
    This functions returns list object containing synonymous codons for given
    codon.
    :param gct: dictionary object containing gc table data.
    :param codon: Codon (string) e.g. AAA
    :return:
    """
    try:
        if gct is None or codon is None:
            # Invalid set of inputs provided
            return None
        for key in gct.keys():
            aa_data = gct.get(key)
            if codon in aa_data["codons"]:
                # found the codon, return AA key.
                return aa_data["codons"]
        # Could not find this codon in any AA's data.
        return None
    except Exception:
        return None
































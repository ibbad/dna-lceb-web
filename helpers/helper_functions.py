"""
This module contains the general helper functions for the application.
"""
import json
import string
import random
import scipy.io
from .gc_data_helpers import get_gc_table, codon_to_aa_gct
from .gc_file_helpers import gc_file_associations


def generate_secret_key(length=32):
    """
    Generates a secret key consisting of ascii characters, special characters
    and digits.
    e.g. IG0Z[00;QEq;Iy.sZp8>16dv)reQ(R8z
    :param: length of key (default=32)
    """
    return ''.join(random.choice(string.ascii_letters +
                                 string.digits +
                                 '!@#$%^&*().,;:[]{}<>?')
                   for _ in range(length))


def get_start_stop_codons():
    """
    This function returns a dictionary with list of locations of start and
    stop codons from
    :return:
    """
    pass


def dna_from_mat(filename=None, path=None):
    """
    This function loads the DNA sequence from a .mat file. if both filename
    and path are provided for file, then path is preferred.
    :param filename: filename(string) e.g., filename.mat. Looked in
    default folder dataset/
    :param path: fully qualified path e.g. /folder/subfolder/filename.mat
    :return: string object containing DNA String.
    """
    if path is not None:
        data = scipy.io.loadmat(path)
        filename = path.split('/')[-1].split('.')[0]
        try:
            return str(data.get(filename)[0])
        except TypeError:
            # Invalid file name extracted from data
            raise TypeError
            return None
        except FileNotFoundError:
            # File not found in default folder
            raise FileNotFoundError
            return None
    elif filename is not None:
        # Read file from default folder
        data = scipy.io.loadmat('dataset/mat/' + filename)
        seq_id = filename.split('.')[0] # Expected_filename= filename.mat
        try:
            return str(data.get(seq_id)[0])
        except FileNotFoundError:
            # File not found in default folder
            raise FileNotFoundError
            return None
    else:
        # Invalid parameters provided.
        print("Invalid parameters")
        return None


def dna_from_json(filename=None, path=None):
    """
    This function loads the DNA sequence from a .json file. if both filename
    and path are provided for file, then path is preferred.
    :param filename: filename(string) e.g., filename.mat. Looked in
    default folder 'dataset/'
    :param path: fully qualified path e.g. /folder/subfolder/filename.mat
    :return: dictionary object containing the string.
    :except TypeError:
    """
    if path is not None:
        try:
            with open(path) as dna_file:
                data = json.load(dna_file)
            return data
        except TypeError:
            # Invalid file name extracted from data
            return TypeError
        except FileNotFoundError:
            # File does not exist on the path
            raise FileNotFoundError
    elif filename is not None:
        try:
            # Read file from default folder
            with open('dataset/json/' + filename) as dna_file:
                data = json.load(dna_file)
            return data
        except TypeError:
            # Invalid file name extracted from data
            raise TypeError
        except FileNotFoundError:
            # File not found in default folder
            raise FileNotFoundError
    else:
        # Invalid parameters provided.
        return None


def find_coding_region(dna_seq=None, gc=1):
    """
    This function returns a dictionary with two lists containing start and
    stop indexes for coding frames in the given dna sequence.
    :param dna_seq: dna sequence string.
    :param gc: genetic code (integer). default=None
    :return: dictionary object containing list of indexes for start and stop
    codons.
    """
    if dna_seq is None or type(dna_seq) is not str:
        # Bad dna_seq value
        return None
    # Read the genetic code table data.
    try:
        # If given gc is not found, use
        gct = get_gc_table(gc_file_associations.get(str(gc)))
        dna = dna_seq[:len(dna_seq) - (len(dna_seq) % 3)]
        dna = _clean_dna(dna)

        # Find the start/stop codon indexes.
        start_index = []
        stop_index = []

        # Flag for start
        start = False
        for i in range(0, len(dna), 3):
            codon = dna[i:i+3]
            # check for codon amino acid and if its MET then mark as start.
            aa = codon_to_aa_gct(gct=gct, codon=codon).lower()
            if aa == 'met' and not start:
                start_index.append(i)
                start = True
            elif aa == 'stop' and start:
                stop_index.append(i)
                start = False
        if len(stop_index) < len(start_index):
            stop_index.append((len(dna)-len(dna) %3) + 1)
        return dict(start=start_index, stop=stop_index)
    except KeyError:
        # given GC value does not have any associated file.
        pass


def _clean_dna(dna_seq):
    """
    This function removes any characters from the dna string if it is not A,
    G,C,T
    :param dna_seq: input dna sequences (string)
    :return:
    """
    return ''.join(c for c in dna_seq.lower() if c in 'agct')




















































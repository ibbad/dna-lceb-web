"""
This module contains the general helper functions for the application.
"""
import json
import string
import random
import scipy.io
from .gc_data_helpers import get_gc_table, codon_to_aa_gct, \
    get_aa_using_codon_gct
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


def find_coding_region(dna_seq=None, frame=1, gc=1):
    """
    This function returns a dictionary with two lists containing start and
    stop indexes for coding frames in the given dna sequence.
    :param dna_seq: dna sequence string.
    :param frame: open reading frame number i.e. 1, 2, 3 default=1
    :param gc: genetic code (integer). default=None
    :return: dictionary object containing list of indexes for start and stop
    codons.
    """
    # TODO: Take open reading frames into account.
    if dna_seq is None or type(dna_seq) is not str:
        # Bad dna_seq value
        return None
    if frame > 3 or frame < 1:
        # Invalid frame number
        return None
    # Read the genetic code table data.
    try:
        # If given gc is not found, use
        gct = get_gc_table(gc_file_associations.get(str(gc)))
        dna_seq = _clean_dna(dna_seq)
        dna = dna_seq[
              (frame - 1): (len(dna_seq) - (len(dna_seq) % 3) + (frame - 1))]

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


def find_capacity(dna_seq=None, frame=1, gc=1):
    """
    This function returns the capacity for given sequence.
    :param dna_seq: dna sequence string.
    :param frame: open reading frame number e.g. 1, 2, 3, default=1
    :param gc: genetic code (integer). default=None
    :return capacity: number of bits we can store in given dna sequence.
    codons.
    """
    if dna_seq is None or type(dna_seq) is not str:
        # Bad dna_seq value
        return None
    if frame > 3 or frame < 1:
        # Bad value for frame
        return None
    # Read the genetic code table data.
    try:
        # If given gc is not found, use
        gct = get_gc_table(gc_file_associations.get(str(gc)))
        dna_seq = _clean_dna(dna_seq)
        dna = dna_seq[
              (frame - 1):(len(dna_seq) - (len(dna_seq) % 3) + (frame - 1))]
        capacity = 0
        # Flag for start
        start = False
        for i in range(0, len(dna), 3):
            codon = dna[i:i+3]
            # check for codon amino acid and if its MET then mark as start.
            aa = get_aa_using_codon_gct(gct=gct, codon=codon)
            if aa["key"] == 'met' and not start:
                start = True
            elif aa["key"] == 'stop' and start:
                if aa["count"] > 3:
                    capacity += 2
                elif aa["count"] > 1:
                    capacity += 1
                start = False
            # include stop codon in watermarking region
            if start:
                if aa["count"] > 3:
                    capacity += 2
                elif aa["count"] > 1:
                    capacity += 1
        return capacity
    except KeyError:
        # given GC value does not have any associated file.
        pass
    except ValueError:
        # count has invalid string value
        pass


def find_capacity_for_coding_region(dna_seq=None, region={}, frame=1, gc=1):
    """
    This function returns the capacity for given sequence.
    :param dna_seq: dna sequence string.
    :param region: dictionary object containing indexes of start and stop codon.
    :param frame: open reading frame number e.g. 1, 2, 3, default=1
    :param gc: genetic code (integer). default=None
    :return capacity: number of bits we can store in given dna sequence.
    codons.
    """
    if dna_seq is None or type(dna_seq) is not str:
        # Bad dna_seq value
        return None
    if frame > 3 or frame < 1:
        # Bad value for frame
        return None
    # Read the genetic code table data.
    try:
        # If given gc is not found, use
        gct = get_gc_table(gc_file_associations.get(str(gc)))
        dna_seq = _clean_dna(dna_seq)
        dna = dna_seq[
              (frame - 1):(len(dna_seq) - (len(dna_seq) % 3) + (frame - 1))]
        capacity = 0
        # TODO: Break down the dna sequencing over a pool of processes.
        for i in range(len(region["start"])):
            if i < len(region["stop"]):
                dna_portion = dna[region["start"][i]: region["stop"][i]]
            else:
                dna_portion = dna[region["start"][i]: len(dna)]

            # calculate capacity
            for j in range(0, len(dna_portion), 3):
                aa = get_aa_using_codon_gct(gct=gct, codon=dna[j: j+3])
                if aa["count"] > 3:
                    capacity += 2
                elif aa["count"] > 1:
                    capacity += 1
        return capacity
    except KeyError:
        # given GC value does not have any associated file.
        pass
    except ValueError:
        # count has invalid string value
        pass


def _clean_dna(dna_seq):
    """
    This function removes any characters from the dna string if it is not A,
    G,C,T
    :param dna_seq: input dna sequences (string)
    :return:
    """
    return ''.join(c for c in dna_seq.lower() if c in 'agct')


def str_to_bits(str_input):
    """
    Convert string to bits
    :param str_input: string input
    :return: string containing bits.
    """
    bit_str = ""
    for ch in str_input:
        bits = bin(ord(ch))[2:]
        bit_str += '00000000'[len(bits):] + bits
    return bit_str


def bits_to_str(bits):
    """
    Convert bits(string) to string
    :param bits: character array (string) containing bits.
    :return: string
    """
    ch_str = ""
    for b in range(0, len(bits), 8):
        ch_str.append(str(bits[b:b+8]))
    return ch_str


def str2bits(str_in):
    """
    Convert string input to bits.
    :param str_in: input string
    :return: bits returned
    """
    result = []
    for c in str_in:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def bits2str(bits):
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)













































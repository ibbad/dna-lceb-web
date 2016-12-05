"""
Helper functions for rest api and web application.
"""
import json
from helpers.gc_file_helpers import gc_file_associations
from helpers.gc_data_helpers import get_aa_using_codon_gct, get_gc_table, \
    codon_to_aa_gct


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
        print("find capacity dna_seq is none or type is not str")
        return None
    if frame > 3 or frame < 1:
        # Bad value for frame
        print("find capacity frame number invalid ")
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
    except Exception as e:
        print(e)
        return None


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
        print("find_capacity_for_coding_region dna_seq is none")
        return None
    if frame > 3 or frame < 1:
        # Bad value for frame
        print("find_capacity_for_coding_region frame number invalid ")
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
    except Exception as e:
        # given GC value does not have any associated file.
        print(e)
        return None


def _clean_dna(dna_seq):
    """
    This function removes any characters from the dna string if it is not A,
    G,C,T
    :param dna_seq: input dna sequences (string)
    :return:
    """
    return ''.join(c for c in dna_seq.lower() if c in 'agct')


def str_to_bin(str_input):
    """
    Convert character string to binary string
    :param str_input: string input
    :return: string containing bits.
    """
    bit_str = ""
    for ch in str_input:
        bits = bin(ord(ch))[2:]
        bit_str += '00000000'[len(bits):] + bits
    return bit_str


def bin_to_str(bits):
    """
    Convert binary string to character string.
    :param bits: character array (string) containing bits.
    :return: string
    """
    ch_str = []
    for b in range(0, len(bits), 8):
        ch_str.append(chr(int(bits[b:b+8], 2)))
    return ''.join([c for c in ch_str])


def bin_to_nucleotide(bin_str):
    """
    Convert binary bits to nucleotide
    :param bin_str: pair of binary bits.
    :return: nulceotide A, G, C, T
    """
    if bin_str == '00':
        return 'A'
    elif bin_str == '01':
        return 'C'
    elif bin_str == '10':
        return 'G'
    elif bin_str == '11':
        return 'T'
    else:
        return None


def nucleotide_to_bin(ch):
    """
    Convert nucleotide to binary string
    :param ch: A, G, C, T
    :return: binary_string: 00, 01, 10, 11
    """
    if ch == 'A':
        return '00'
    elif ch == 'C':
        return '10'
    elif ch == 'G':
        return '10'
    elif ch == 'T':
        return '11'
    else:
        return None


def _lsb_4fold(aa, bits):
    """
    This function embeds a pair of bits in 4/5/6 fold degenerative codon.
    :param aa: amino acid information.
    :param bits: bits (string of length 2 e.g. 00) which should be
    embedded in codon.
    :return: watermarked codon (string) e.g. AGA.
    """
    codon = _find_popular_codon(aa)
    if bits == '00':
        return codon[:2]+'a'
    elif bits == '01':
        return codon[:2]+'c'
    elif bits == '10':
        return codon[:2]+'g'
    elif bits == '11':
        return codon[:2]+'t'
    else:
        print(aa, bits)
        return None


def _lsb_2fold(aa, bit):
    """
    This function embeds a pair of bits in 2/3 fold degenerative codon.
    :param aa: amino acid information.
    :param bit: bit (character 2 e.g. 0) which should be embedded in codon.
    :return: watermarked codon (string) e.g. AGA.
    """
    if bit == '0':
        return aa["codons"][0]
    else:
        return aa["codons"][1]


def _extract_2fold(codon, aa):
    """
    This function embeds a pair of bits in 2/3 fold degenerative codon.
    :param codon: watermarked codon
    :param aa: amino acid information.
    :return: extracted bit 0 or 1.
    """
    if codon == aa["codons"][0].lower():
        return '0'
    else:
        return '1'


def _extract_lsb_4fold(codon):
    """
    This function returns a pair of bits from LSB of 4 fold synonymous
    substitution codon.
    :param codon: codon from which, message needs to be extracted.
    :return: a pair of binary bits (string format) extracted from LSB of
    given codon.
    """
    if codon[-1] == 'a':
        return '00'
    elif codon[-1] == 'c':
        return '01'
    elif codon[-1] == 'g':
        return '10'
    elif codon[-1] == 't':
        return '11'
    else:
        print(codon)
        return None


def _find_popular_codon(aa):
    """
    This function returns popular codon from a 4+ fold degenerative codon.
    :param aa: dictionary containing amino acid information.
    :return:
    """
    codons = [c[:2] for c in aa["codons"]]
    counts = []
    for i in range(len(codons)):
        pc = codons[i]
        count = 0
        for j in range(len(codons)):
            if codons[j] == pc:
                count += 1
        counts.append(count)
    # find index of the higest entry
    highest = 0
    for i in range(len(counts)):
        if counts[i] > counts[highest]:
            highest = i
    return aa["codons"][highest]


def _int_to_bin_str(value):
    """
    This function returns the integer value in binary string of length 16.
    :param value: integer value to be converted to binary string.
    :return: None if 0 > value > 2^16-1
    """
    if 0 < value < (2**16):
        bits = bin(value)[2:]
        return ('0'*16)[len(bits):] + bits
    else:
        print("None in int2binstr")
        None


def _bin_str_to_int(bin_str):
    """
    This function returns integere value extracted from binary string of
    length 16.
    :param bin_str:
    :return:
    """
    if len(bin_str) <= 16:
        return int(bin_str, 2)
    else:
        None


def embed_data(dna_seq=None, message=None, frame=1, region={}, gc=1):
    """
    This function embeds the given message in given DNA sequence.
    :param dna_seq: DNA sequence (string) to be watermarked.
    :param message: watermark message (string)
    :param frame: open reading frame number in which data will be
    watermarked.
    :param region: dictionary containing position of start, stop codons
    for coding regions.
    :param gc: genetic code.
    :return: DNA sequence (string) watermarked.
    """
    if dna_seq is None or type(dna_seq) is not str:

        print("embed_data frame number invalid ")
        return None
    # Clean dna sequence.
    dna_seq = _clean_dna(dna_seq)
    wm_dna = ""                             # watermarked DNA
    # embed data
    try:
        # Convert data to binary string
        wm_len = _int_to_bin_str(len(message))
        wmc = 0                             # watermark counter
        wm_data = str_to_bin(message)
        wm_data = wm_len + wm_data  # append length to wm data.
        gct = get_gc_table(gc_file_associations.get(str(gc)))
        dna = dna_seq[
              (frame-1): (len(dna_seq) - (len(dna_seq) % 3) + (frame - 1))]

        # Finish last coding region at the end of DNA.
        if len(region.get("start")) < len(region.get("stop")):
            region.get("stop").append(len(dna))
        rc = 0
        i = 0
        while i < len(dna):
            # Loop through whole DNA sequence with step size = 3 (i.e. length
            #  of codon)
            if rc < len(region.get("start")) and i >= region.get("start")[rc]:
                # Loop through coding region.
                j = i
                while j < region.get("stop")[rc] - 3:
                    # embed data
                    aa = get_aa_using_codon_gct(gct=gct, codon=dna[j: j+3])
                    if aa["count"] > 3 and wmc < len(wm_data):
                        # embedding in 4+ fold codons
                        if wmc == len(wm_data) - 1:
                            # fail safe condition if we have one bit left to
                            # embed and available codon is 4+ fold.
                            wm_dna += _lsb_4fold(aa=aa,
                                                 bits=wm_data[wmc]+'0')
                            wmc += 1
                        else:
                            wm_dna += _lsb_4fold(aa=aa, bits=wm_data[wmc:wmc+2])
                            wmc += 2
                    elif aa["count"] > 1 and wmc < len(wm_data):
                        # embedding in 2/3 fold codons
                        wm_dna += _lsb_2fold(aa=aa, bit=wm_data[wmc])
                        wmc += 1
                    else:
                        wm_dna += dna[j:j+3]
                    j += 3
                rc += 1          # update rc for next coding region.
                i = j            # increment counters accordingly
            else:
                # if not in coding region
                wm_dna += dna[i:i+3]
                i += 3
        # append the remaining sequence.
        if len(wm_dna) < len(dna_seq):
            wm_dna += dna_seq[len(wm_dna):]
        return wm_dna.lower()
    except ValueError as e:
        print(e)
        return None


def extract_data(wm_dna=None, frame=1, region={}, gc=1):
    """
    This function embeds the given message in given DNA sequence.
    :param wm_dna: watermarked DNA sequence (string) to be watermarked.
    :param frame: open reading frame number in which data will be
    watermarked.
    :param region: dictionary containing position of start, stop codons
    for coding regions.
    :param gc: genetic code.
    :return: DNA sequence (string) watermarked.
    """
    if wm_dna is None or type(wm_dna) is not str:
        print("extract_data wm_dna is none or type is not str")
        return None
    # Clean dna sequence.
    dna_seq = _clean_dna(wm_dna)
    # extract data
    try:
        # Convert data to binary string
        wm_msg = ""
        gct = get_gc_table(gc_file_associations.get(str(gc)))
        dna = dna_seq[
              (frame-1): (len(dna_seq) - (len(dna_seq) % 3) + (frame - 1))]

        # Finish last coding region at the end of DNA.
        if len(region.get("start")) < len(region.get("stop")):
            region.get("stop").append(len(dna))
        rc = 0
        i = 0
        while i < len(dna):
            # Loop through whole DNA sequence with step size = 3 (i.e. length
            #  of codon)
            if rc < len(region.get("start")) and i >= region.get("start")[rc]:
                # Loop through coding region.
                j = i
                while j < region.get("stop")[rc] - 3:
                    # extract data
                    aa = get_aa_using_codon_gct(gct=gct, codon=dna[j: j+3])
                    if aa["count"] > 3:
                        # extract from 4+ fold codons
                        wm_msg += _extract_lsb_4fold(codon=dna[j: j+3])
                    elif aa["count"] > 1:
                        # extract from 2/3 fold codons
                        wm_msg += _extract_2fold(codon=dna[j:j+3], aa=aa)
                    else:
                        pass     # skip
                    j += 3
                rc += 1          # update rc for next coding region.
                i = j            # increment counters accordingly
            else:
                i += 3           # skip non coding region
        # get length from data from first 16 bits
        wm_len = _bin_str_to_int(wm_msg[0:16])
        # convert and return the watermark data
        return bin_to_str(wm_msg[16:(16+wm_len*8)])
    except Exception as e:
        print(e)
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
        print("find_coding_region dna_seq is none")
        return None
    if frame > 3 or frame < 1:
        # Invalid frame number
        print("find_coding_region frame is invalid")
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
                stop_index.append(i+3)
                start = False
        if len(stop_index) < len(start_index):
            stop_index.append((len(dna)-len(dna) % 3) + 1)
        return dict(start=start_index, stop=stop_index)
    except Exception as e:
        print(e)
        return None


def get_filenames_from_directory(directory='dataset/json'):
    """
    This function reads name of all test sequences in dataset/json category
    and returns in form of a list.
    :param directory: path to directory from where the files must be read.
    :return:
    """
    from os import walk
    files = []
    for (dirpath, dirnames, filenames) in walk(directory):
        files.extend(filenames)
        break
    return files


def load_sequence_choices(file_path='dataset/json/directory.json'):
    """
    This function returns the directory file and loads the filenames and
    associated json codes into a list of tuples.
    :param file_path: path of directory file
    :return:
    """
    try:
        data = dict()

        with open(file_path) as directory_file:
            data = json.loads(directory_file)
        choices = []
        for key in data:
            choices.extend((key, data.get(key)))

    except FileNotFoundError:
        return []









































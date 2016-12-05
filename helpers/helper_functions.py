"""
This module contains the general helper functions for the application.
"""
import json
import string
import random
import scipy.io


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


def dna_from_mat(filename=None, file_path=None):
    """
    This function loads the DNA sequence from a .mat file. if both filename
    and path are provided for file, then path is preferred.
    :param filename: filename(string) e.g., filename.mat. Looked in
    default folder dataset/
    :param path: fully qualified path e.g. /folder/subfolder/filename.mat
    :return: string object containing DNA String.
    """
    if file_path is not None:
        data = scipy.io.loadmat(file_path)
        filename = file_path.split('/')[-1].split('.')[0]
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
        seq_id = filename.split('.')[0]    # Expected_filename= filename.mat
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


def dna_from_json(filename=None, file_path=None):
    """
    This function loads the DNA sequence from a .json file. if both filename
    and path are provided for file, then path is preferred.
    :param filename: filename(string) e.g., filename.mat. Looked in
    default folder 'dataset/'
    :param path: fully qualified path e.g. /folder/subfolder/filename.mat
    :return: dictionary object containing the string.
    :except TypeError:
    """
    if file_path is not None:
        try:
            with open(file_path) as dna_file:
                data = json.load(dna_file)
            return data
        except TypeError:
            # Invalid file name extracted from data
            return TypeError
        except FileNotFoundError as e:
            print(file_path)
            print(filename)
            # File not found in default folder
            print(e)
            # File does not exist on the path
            raise FileNotFoundError
    elif filename is not None:
        try:
            # Read file from default folder
            with open('dataset/json/' + filename) as dna_file:
                data = json.load(dna_file)
            return data
        except TypeError as e:
            # Invalid file name extracted from data
            print(e)
            raise TypeError
        except FileNotFoundError as e:
            print(file_path)
            print(filename)
            # File not found in default folder
            print(e)
            raise FileNotFoundError
    else:
        # Invalid parameters provided.
        return None


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


def str2bits(str_in):
    """
    Convert string input to bits.
    :param str_in: input string
    :return: bits array
    """
    result = []
    for c in str_in:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result


def bits2str(bits):
    """
    Convert binary array to string.
    :param bits: bit array.
    :return: character string.
    """
    chars = []
    for b in range(int(len(bits) / 8)):
        byte = bits[b * 8:(b + 1) * 8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


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
        with open(file_path) as directory_file:
            data = json.load(directory_file)
        choices = []
        for key in data:
            choices.append((key, data.get(key)['name']))
        return choices
    except FileNotFoundError:
        return []


def get_chosen_file_path(file_path='dataset/json/directory.json', key=None):
    """
    This function returns the name of file which is selected from list of
    default methods.
    :param file_path: path to file from where the filename should be read
    against a given key.
    :param key: key for which the data must be read.
    :return: path to the file (relative to app directory tree.)
    """
    try:
        print(file_path)
        with open(file_path) as data_file:
            data = json.load(data_file)
        return data.get(key)['filePath']
    except FileNotFoundError:
        return None
    except Exception:
        return None


def get_chosen_file_name(file_path='dataset/json/directory.json', key=None):
    """
    This function returns the name of file which is selected from list of
    default methods.
    :param file_path: path to file from where the filename should be read
    against a given key.
    :param key: key for which the data must be read.
    :return: path to the file (relative to app directory tree.)
    """
    try:
        print(file_path)
        with open(file_path) as data_file:
            data = json.load(data_file)
        return data.get(key)['fileName']
    except FileNotFoundError:
        return None
    except Exception:
        return None



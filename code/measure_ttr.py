import csv
import progressbar
import re
import tarfile
from utils import list_tar_files, read_lines_from_tar_file
from collections import namedtuple
from os.path import getsize
from pathlib import Path
from statistics import mean 

# declare all the named tuples up front
TTR = namedtuple('TTR', 'TTR MATTR500 MATTR1k ATTR AMATTR500 AMATTR1k')
# https://stackoverflow.com/questions/4800665
pattern = re.compile(u'^[^\W\d_]+$', re.UNICODE)

def measure_ttr(corpus):
    """
    Captures the measures of diversity as below:

    * Type/Token Ratio
    * Moving Average Type/Token Ratio in 500 and 1k versions
    * Adjusted versions of the above to include neither punctuation nor numeric words

    This measure assumes the below:
    
    * Words are seperated by a space

    Parameters
    ----------
    corpus : str
        The tarball containing pre-tokenized text only files.

    Example
    ----------
    import measure_ttr; measure_ttr.measure_ttr('../data/tokenized.tar')
    """
    corpus = Path(corpus)

    measure = corpus.parent.joinpath('./diversity.csv')
    if measure.exists():
        measure.unlink()

    widgets = [ 'Measuring: ', progressbar.Percentage(), ' ', progressbar.Bar(marker = '.', left = '[', right = ']'), ' ', progressbar.ETA() ]

    with progressbar.ProgressBar(widgets = widgets, max_value = getsize(corpus)) as bar:
        with tarfile.open(corpus, 'r') as corpus:
            with open(measure, 'w', encoding = 'utf-8', newline = '') as measure:
                measure = csv.writer(measure, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)    
                measure.writerow(['id', 'TTR','MATTR500','MATTR1k','ATTR','AMATTR500','AMATTR1k'])
                for (tar_info, tar_file) in list_tar_files(corpus):
                    id = Path(tar_info.name).stem
                    lines = read_lines_from_tar_file(tar_file)
                    m = calculate_measure(lines)
                    measure.writerow([id, m.TTR, m.MATTR500, m.MATTR1k, m.ATTR, m.AMATTR500, m.AMATTR1k])
                    bar.update(tar_info.offset_data + tar_info.size)
                pass
            pass
        pass
    pass

def calculate_measure(lines):
    
    lines = [x.strip() for x in lines]
    lines = [x.split() for x in lines if len(x) > 0]

    # https://stackoverflow.com/questions/952914
    flat_list = [item for sublist in lines for item in sublist]
    adj_flat_list = filter_out_nonwords(flat_list)

    ttr = calculate_mattr(flat_list, len(flat_list))
    mattr500 = calculate_mattr(flat_list, 500)
    mattr1k = calculate_mattr(flat_list, 1000)

    attr = calculate_mattr(adj_flat_list, len(adj_flat_list))
    amattr500 = calculate_mattr(adj_flat_list, 500)
    amattr1k = calculate_mattr(adj_flat_list, 1000)
    
    return TTR(round(ttr, 3), round(mattr500, 3), round(mattr1k, 3), round(attr, 3), round(amattr500, 3), round(amattr1k, 3))

def calculate_mattr(word_list, window_length):

    if len(word_list) == 0:
        pass
        return 0
    elif len(word_list) <= window_length:
        ttr = len(set(word_list)) / len(word_list)
        return ttr
    else:
        ttr = [0] * (len(word_list) - window_length + 1)
        ttr_pos = 0
        dict = {}
        for i in range(0, window_length):
            pass
            plus_one(dict, word_list[i])
        ttr[ttr_pos] = len(dict)
        ttr_pos = ttr_pos + 1
        for i in range(window_length, len(word_list)):
            minus_one(dict, word_list[i - window_length])
            plus_one(dict, word_list[i])
            ttr[ttr_pos] = len(dict)
            ttr_pos = ttr_pos + 1
        return mean(ttr)/window_length

def plus_one(frequency_dict, item):

    if item in frequency_dict:
        pass
        frequency_dict[item] = frequency_dict[item] + 1
    else:
        pass
        frequency_dict[item] = 1
    pass

def minus_one(frequency_dict, item):

    count = frequency_dict[item]
    if count > 1:
        pass
        frequency_dict[item] = count - 1
    else:
        pass
        del frequency_dict[item]

def filter_out_nonwords(token_list):

    filtered_list = [token for token in token_list if isword(token)]    
    return filtered_list

def isword(token):

    return pattern.match(token)

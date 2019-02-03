import csv
import progressbar
import tarfile
from utils import list_tar_files, read_lines_from_tar_file
from collections import namedtuple
from os.path import getsize
from pathlib import Path
from statistics import mean 

# declare all the named tuples up front
CAD = namedtuple('CAD', 'Words Sentences Paragraphs')

def measure_cadence(corpus):
    """
    Captures the measures of cadence as below:

    * Total Words
    * Total Sentences
    * Total Paragraphs

    This measure assumes the below:
    
    * Words are seperated by a space
    * 1 sentence per line
    * 2 neighboring sentences are from distinct paragraphs iff seperated by a blank line

    Parameters
    ----------
    corpus : str
        The tarball containing pre-tokenized text only files.

    Example
    ----------
    import measure_cadence; measure_cadence.measure_cadence('../data/tokenized.tar')
    """
    corpus = Path(corpus)

    measure = corpus.parent.joinpath('./cadence.csv')
    if measure.exists():
        measure.unlink()

    widgets = [ 'Measuring: ', progressbar.Percentage(), ' ', progressbar.Bar(marker = '.', left = '[', right = ']'), ' ', progressbar.ETA() ]

    with progressbar.ProgressBar(widgets = widgets, max_value = getsize(corpus)) as bar:
        with tarfile.open(corpus, 'r') as corpus:
            with open(measure, 'w', encoding = 'utf-8', newline = '') as measure:
                measure = csv.writer(measure, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_ALL)    
                measure.writerow(['id', 'Words', 'Sentences', 'Paragraphs'])
                for (tar_info, tar_file) in list_tar_files(corpus):
                    id = Path(tar_info.name).stem
                    lines = read_lines_from_tar_file(tar_file)
                    m = calculate_measure(lines)
                    measure.writerow([id, m.Words, m.Sentences, m.Paragraphs])
                    bar.update(tar_info.offset_data + tar_info.size)
                pass
            pass
        pass
    pass

def calculate_measure(lines):

    lines = [len(x.split()) for x in lines]

    tw = sum(lines)
    ts = sum(1 for x in lines if x > 0)
    tp = sum(1 for x in lines if x == 0) + 1
    
    return CAD(tw,  ts, tp)

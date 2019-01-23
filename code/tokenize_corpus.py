import pathlib
import progressbar
import tarfile
from utils.tarfile import list_tar_files
from io import BytesIO
from nltk.tokenize import word_tokenize, sent_tokenize
from os.path import getsize

def tokenize_corpus(converted_tarball):
    """
    Tokenizes all the text only files in a tarball into the standard form I use for text processing

    Parameters
    ----------
    converted_tarball : str
        The tarball containing text only files
    """
    converted_tarball = pathlib.Path(converted_tarball)

    tokenized_tarball = converted_tarball.parent.joinpath('./tokenized.tar')
    if tokenized_tarball.exists():
        tokenized_tarball.unlink()

    widgets = [ 'Tokenizing: ', progressbar.Percentage(), ' ', progressbar.Bar(marker = '.', left = '[', right = ']'), ' ', progressbar.ETA() ]

    with progressbar.ProgressBar(widgets = widgets, max_value = getsize(converted_tarball)) as bar:
        with tarfile.open(converted_tarball, 'r') as converted_tarball:        
            with tarfile.open(tokenized_tarball, 'w') as tokenized_tarball:
                for (tar_info, tar_file) in list_tar_files(converted_tarball):
                    text_only_file = read_text_only_file(tar_file)
                    tokenized_file = tokenize_file(text_only_file)
                    write_tokenized_file(tokenized_tarball, tar_info, tokenized_file)
                    bar.update(tar_info.offset_data + tar_info.size)
                pass
            pass
        pass
    pass

def read_text_only_file(tar_file):
    """
    Read the tar file returning the lines
    """

    txt = tar_file.read()
    txt = txt.decode('utf-8')
    txt = txt.splitlines()
    return txt

def tokenize_file(text_only_file):
    """
    Tokenizes a single file
    """

    for line in text_only_file:
        line = line.strip()
        if line == '':
            yield ''
            pass
        else:
            sentences = sent_tokenize(line)
            for sentence in sentences:
                words = word_tokenize(sentence)
                yield ' '.join(words)
            pass
        pass
    pass

def write_tokenized_file(tokenized_tarball, tar_info, tokenized_file):
    """
    Writes the relevant wmd data to the tar ball
    """

    txt = '\n'.join(tokenized_file)
    txt = txt.encode('utf-8')
    with BytesIO(txt) as tar_file:
        info = tarfile.TarInfo(name = tar_info.name)
        info.size = len(txt)
        tokenized_tarball.addfile(info, fileobj = tar_file)
    pass

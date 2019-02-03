import progressbar
import tarfile
from utils import list_tar_files, read_lines_from_tar, write_lines_to_tarball
from nltk.tokenize import word_tokenize, sent_tokenize
from os.path import getsize
from pathlib import Path

def tokenize_corpus(corpus):
    """
    Tokenizes all the text only files in a tarball into the standard form I use for text processing

    Parameters
    ----------
    corpus : str
        The tarball containing text only files
    """
    corpus = Path(corpus)

    tokenized_tarball = corpus.parent.joinpath('./tokenized.tar')
    if tokenized_tarball.exists():
        tokenized_tarball.unlink()

    widgets = [ 'Tokenizing: ', progressbar.Percentage(), ' ', progressbar.Bar(marker = '.', left = '[', right = ']'), ' ', progressbar.ETA() ]

    with progressbar.ProgressBar(widgets = widgets, max_value = getsize(corpus)) as bar:
        with tarfile.open(corpus, 'r') as corpus:        
            with tarfile.open(tokenized_tarball, 'w') as tokenized_tarball:
                for (tar_info, tar_file) in list_tar_files(corpus):
                    lines = read_lines_from_tar(tar_file)
                    lines = undo_word_wrap(lines)
                    lines = tokenize_lines(lines)
                    write_lines_to_tarball(tokenized_tarball, tar_info, lines)
                    bar.update(tar_info.offset_data + tar_info.size)
                pass
            pass
        pass
    pass

def undo_word_wrap(lines):
    """
    Undo manual word wrap
    """

    last = None
    for line in lines:
        line = line.strip()
        if line == '':
            yield last
            yield ''
            last = None
        elif last == None:
            pass
            last = line
        else:
            pass
            last = last + ' ' + line
        pass

    if last != None:
        pass
        yield last

    pass

def tokenize_lines(lines):
    """
    Tokenizes all the lines using the standard Punkt + PENN TreeBank tokenizer
    """

    for line in lines:
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

tokenize_corpus('../data/corpus.tar')
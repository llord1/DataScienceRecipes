# Document Collection

Most collections of documents require a special collection method.
Pawning this task off to your research assistant is O.K., but make sure you do it with them for a little while.
This is because it is important that the full corpus be in a similar format.
Also, aggreators are your friends here as they tend to do this kind of thing for you.
When you use an aggreator, you are generaly best off writing a script.

All the documents for this analysis are from [Project Gutenberg][gutenberg].
An astute observer will notice that each of the books is broken down into one chapter per document.
This is not normaly done.
It was preformed in this case to increase the number of data points.

[GitHub](https://github.com) does not like you hosting [_large_ files](https://help.github.com/articles/conditions-for-large-files/).
Explore other options storage options after you aquire the documents.
Even today (2019), I find sneakernet works quite well when dealing with multi-GB files.
If everyone in your group _really_ needs access to the raw files and not just the measures, consider a cloud service.
A VM in [Azure](https://azure.microsoft.com/en-us/services/virtual-machines/) is pretty cheap and it doubles as a shared compute device.
Just remember to turn it off when you are not using it.

# Feature Collection

R is not super great at analysing large corpuses so this process is run in Pure Python.
In a shell window, change to the `./code` folder and run the below commands.
Some pathing or name correction may be necessary.

A single TAR file is useful in this context because as the number of documents in the corpus expands, a simple directory containing all of them becomes unwieldy.
The documents in `corpus.tar` should be plain text without markup or other forms of notation.
The general format of the documents should be:

* Tokens seperated by 1 space.
  * In this context tokens mean both words and symbols.
    This is done up front to prevent re-seperating out all the '.'s before we collect the measures.
* One sentence per line.
* Paragraphs seperated by a single blank line.

As our source comes from [Project Gutenberg][gutenberg], the sentences need to be recombined.
`tokenize_corpus()` puts all the documents into the expected format.
If you get the documents with different formats, they need to be normalized before measures are taken.
So you may need to modify `tokenize_corpus()` to suit your purpose.

```{shell}
python -c "import tokenize_corpus; tokenize_corpus.tokenize_corpus('../data/corpus.tar')"
python -c "import measure_cadence; measure_cadence.measure_cadence('../data/tokenized.tar')"
python -c "import measure_ttr; measure_ttr.measure_ttr('../data/tokenized.tar')"
```

[gutenberg]: https://www.gutenberg.org
# Feature Collection

R is not super great at analysing large corpuses so this process is run in Pure Python.
In a shell window, change to the `./code` folder and run the below commands.
Some pathing or name correction may be necessary.

A single TAR file is useful in this context because as the number of documents in the corpus expands, a simple directory containing all of them becomes unwieldy.
The documents in `corpus.tar` should be plain text without markup or other forms of notation. 

```{shell}
python -c "import tokenize_corpus; tokenize_corpus.tokenize_corpus('../data/corpus.tar')"
```




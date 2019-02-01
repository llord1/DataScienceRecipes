# Raison d'etre

> Provide a super fast way to get up and running on a publication using a standard analysis.

I have found myself doing a lot of copy-pasteing recently.
When I collaborate with others, I find myself providing the same type of advice, doing the same types of analysis, only applied to their domain.
I wanted to be able to provide a pre-started 'product' when we start to help focus the conversation.

# How to

## Prerequsits

Download the repo (which encompasses all the files on this site) by clicking the `Clone or Download` button and select `Download ZIP`.
This will download a ZIP file of the entire site on your local computer.
Unzip the folder.

You will also need to have the following installed on your computer:

1. [RStudio][rstudio]
2. [Python][python]
3. A LaTeX Distribution like [TeXLive](https://www.tug.org/texlive) or [MikTeX](https://miktex.org)
4. Fonts used in the template
   [1](https://github.com/georgd/EB-Garamond),
   [2](https://github.com/adobe-fonts/source-code-pro),
   [3](http://www.latofonts.com/lato-free-fonts)
5. A few R packages
   [1](https://CRAN.R-project.org/package=bookdown),
   [2](https://CRAN.R-project.org/package=devtools),
   [3](https://CRAN.R-project.org/package=dplyr),
   [4](https://CRAN.R-project.org/package=ggplot2),
   [5](https://CRAN.R-project.org/package=kableExtra),
   [6](https://CRAN.R-project.org/package=knitr),
   [7](https://CRAN.R-project.org/package=readr)

## File off the serial numbers

In order to make this repo function as a big red eazy button, I had to fill out a lot of information.
Some of that information is unique to me, so you probaly want to put your name on it instead.

* Change your `./LICENSE` file to the [MIT license](https://choosealicense.com/licenses/mit).
  I use [CC0](https://choosealicense.com/licenses/cc0) here because this work is ment to be cook book level super generic.
  Your work probaly has something that makes it special.
* Remove this `./README.md` and put in your timeline and tasks as `- [ ] {{task name}}`.
  Making checklists seems super helpful.
* Choose an appropriate type of analysis for your work from the `./analysis/` folder.
  Delete the rest.
  Delete the corsponding `./paper/40-{analysis}.rmd` files.
  Delete the corsponding `./paper/50-{analysis}.rmd` files.
  If you want to do more than one type of analysis, just delete the ones you _don't_ want.
  Remember:
  * Theory drives hypothesis
  * Hypothesis drives data collection
  * Data collection drives analysis
* For each `.rmd` file in the `./analysis` folder:
  * Remove my name.
    Put in your own name(s).
* In `./paper/index.rmd`:
  * Put in your working title in the `title` tag.
  * Remove my name.
    Put in your own name(s).
  * Select the correct `csl` for your journal.
  * Update the `url` and `github-repo` tags to your your repo's name.
    Remove the tags if you don't use [GitHub][github].
* In the other `./paper/*.rmd` files:
  * Replace the [Latin copy text][ipsum].
  * Reword or remove the non-[Latin copy text][ipsum].
    In general, I like to cite the algorithms used because I find it helpful for new readers.
	Because of this, I chose citations that are generic and may be only tangentaly related to your efforts.
	Your group may not be overly concerned about this or want to find more on-point refrences.
* In `./paper/_bookdown.yml`:
  * Update the `repo` tag to your your repo's name.
    Remove the tag if you don't use [GitHub][github].
* In `./litreview/.gitignore`:
  * Uncomment line 2.

# Hints and advice

1. Rendering to PDF can get wierd with page breaks and wraping.
   Add a single line with `\clearpage` to force a page break.
   It will not fix everything, but it usually goes a long way.
2. Do all your work in the `./analysis/{{analysis type}}` file first.
   After your group agrees on the results, then knit the whole thing into a PDF.
   `./analysis` knits are fast, `./paper` knits are slow.
3. [GitHub][github] now allows unlimited private repos.
   Use it.
4. Add in all your lititure review PDFs into the `./litreview` folder to share everything among your group.
   When you fine a new prior work, imideatly save the citation in `./litreview/references.bib`.
   `bookdown` automaticaly prunes unused refrences, and writing the correct citation right before publication is _always_ a hasle.
5. If you flip your repo from private to public, remove all the PDFs and [purge](https://help.github.com/articles/removing-sensitive-data-from-a-repository/) first.
   Different articles have different licenses.
   While you might have the right to the full-text of a work, someone else may not.
   Best to keep just the `references.bib`.
6. All of the `./code` here is a striped down version of what I used in my [dissertation](https://github.com/markanewman/AlgorithmicallyAssistedWriting).
   Looking there might help inspire you to do something special.

## Thanks

This work draws inspiration from several places.
This list is likely incomplete, but attempts to credit those that came before.

> "If I have seen further, it is because I stand on the shoulders of giants."

* [Andrew Zieffler](https://ccaps.umn.edu/andrew-zieffler) [github](https://github.com/zief0002/predissertation-paper) for giving me the idea to 'productize' my other works.
* [Yihui Xie](https://bookdown.org/yihui/bookdown/) for his work on `r markdown` and `bookdown`, the work-horse beneath _all_ of R's pretty formating.
* [RStudio Team][rstudio] because R is so much better at doing statistical analysis than any other language.
  RStudio's presentation of R is just superb.
   
# License

<p xmlns:dct="http://purl.org/dc/terms/">
  <a rel="license"
     href="http://creativecommons.org/publicdomain/zero/1.0/">
    <img src="http://i.creativecommons.org/p/zero/1.0/88x31.png" style="border-style: none;" alt="CC0" />
  </a>
  <br />
  To the extent possible under law,
  <span rel="dct:publisher" resource="[_:publisher]">the person who associated CC0</span>
  with this work has waived all copyright and related or neighboring
  rights to this work.
</p>

[github]: https://github.com
[rstudio]: https://www.rstudio.com
[python]: https://www.python.org
[ipsum]: https://en.wikipedia.org/wiki/Lorem_ipsum
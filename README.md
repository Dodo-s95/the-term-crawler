# The Term Crawler
This repository provides the code for two sequence tagging systems, created with the final aim of tagging terms present in a textual corpus using the BIO tag set. It can be easly adapted to tag using another notation, or to tag other entities.

This code is specifically made to retrieve and tag a corpus and train and test models with the BIO notation on the specific field of swimming.

## Installation
The following command installs all necessary packages:

`pip install -r requirements.txt`

The project was tested using Python 3.8.0.

## Dataset
The dataset can be extracted by running [scraper.py](https://github.com/Dodo-s95/the-term-crawler/blob/main/scraper.py), and converted into usable txt files by running [converter.py](https://github.com/Dodo-s95/the-term-crawler/blob/main/converter.py).

## Terms Extraction
To extract the terms from the corpus we used [TermSuite](http://termsuite.github.io/). We cleaned the first extraction using [term_cleaner.ipynb](https://github.com/Dodo-s95/the-term-crawler/blob/main/term_cleaner.ipynb), and manually validated the outcome. The final extracted list of terms can be found in 

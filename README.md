# The Term Crawler
This repository provides the code for two sequence tagging systems, created with the final aim of tagging terms present in a textual corpus using the BIO tag set. It can be easly adapted to tag using another notation, or to tag other entities.

This code is specifically made to retrieve and tag a corpus and train and test models with the BIO notation on the specific field of swimming.

## Installation
After cloning this repository, you should install the required packages:

`pip install -r requirements.txt`

The project was tested with Python 3.8.0.

## Running the code

### Dataset Extraction
The dataset can be extracted by running [scraper.py](https://github.com/Dodo-s95/the-term-crawler/blob/main/scr/scraper.py), and converted into usable txt files by running [converter.py](https://github.com/Dodo-s95/the-term-crawler/blob/main/scr/converter.py).

### Terms Extraction
To extract the terms from the corpus we used [TermSuite](http://termsuite.github.io/). We cleaned the [first extraction](https://github.com/Dodo-s95/the-term-crawler/blob/main/extractions/swimming-terms_spec_top3k.tsv) using [term_cleaner.ipynb](https://github.com/Dodo-s95/the-term-crawler/blob/main/scr/term_cleaner.ipynb), and manually validated the [outcome](https://github.com/Dodo-s95/the-term-crawler/blob/main/extractions/clean_extraction.csv), also adding and removing some entries. This is the [final list of terms](https://github.com/Dodo-s95/the-term-crawler/blob/main/extractions/swimming-terms_FINAL.tsv).

### Rule-Based Tagging
The [rule-based tagger](https://github.com/Dodo-s95/the-term-crawler/blob/main/scr/rule_based_tagger.ipynb) will tag the corpus you extracted previously using the BIO notation. It will also split the dataset into train, validation and test sets. These silver tagged data will be used to train the neural sequence tagger.

### Neural Tagging
The [neural term-tagger](https://github.com/Dodo-s95/the-term-crawler/blob/main/scr/sequence-tagger.ipynb) is based on `flair`. To train the model you will just need a BIO tagged corpus and run the code as it is. The best model will be automatically saved in a folder of your choosing.

### Inspection of Results
To inspect the results and compare the outputs of the two taggers, we [wrapped](https://github.com/Dodo-s95/the-term-crawler/blob/main/scr/rule_based_wrapper.py) the rule-based tagger and created [testing.ipynb](https://github.com/Dodo-s95/the-term-crawler/blob/main/scr/testing.ipynb). In this latter file, it is enough to input a new text, and you will have the output of the two taggers, ready to be compared.

import spacy
import csv
import pandas as pd
import glob

from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex

from numpy import nan

'''Support file for easy result checking'''


def read_tsv(link):
    with open(link, "r", encoding="utf-8") as tsvfile:
        reader = csv.reader(tsvfile, delimiter="\t")
        return {row[0] for row in reader}

def rule_based_tagger(sentence):

    nlp = spacy.load("en_core_web_sm")

    infixes = (
        LIST_ELLIPSES
        + LIST_ICONS
        + [
            r"(?<=[0-9])[+\-\*^](?=[0-9-])",
            r"(?<=[{al}{q}])\.(?=[{au}{q}])".format(
                al=ALPHA_LOWER, au=ALPHA_UPPER, q=CONCAT_QUOTES
            ),
            r"(?<=[{a}]),(?=[{a}])".format(a=ALPHA),
            r"(?<=[{a}0-9])[:<>=/](?=[{a}])".format(a=ALPHA),
        ]
    )

    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer

    terms_lexicon = read_tsv("../extractions/swimming-terms_FINAL.tsv")

    corpus = sentence

    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    doc = nlp(corpus, disable=['ner', 'parser'])

    df = pd.DataFrame([item for sub in [[tok.text for tok in s]+['<eos>'] for s in doc.sents] for item in sub], columns=["token"])
    df["lemma"] = [item for sub in [[token.lemma_.lower() if token.lemma_ != '-PRON-' else token.lower_ for token in s]+['<eos>'] for s in doc.sents] for item in sub]

    df["tag"] = df["token"].apply(lambda x: nan if x == "<eos>" else "O")
    df["token"] = df["token"].apply(lambda x: nan if x == "<eos>" else x)

    max_term_len = max([len(x.split(" ")) for x in terms_lexicon])

    ngram_df_entries = []

    for i in range(1,max_term_len+1):
        for j in range(len(df)):
            if j+i > len(df):
                pass
            n_gram = ' '.join(df.iloc[j: j+i]["lemma"])
            if n_gram in terms_lexicon:
                ngram_df_entries.append([j, n_gram, i])


    ngram_df = pd.DataFrame(columns=["starting_index", "ngram", "ngram_len"], data=ngram_df_entries)

    ngram_df["is_duplicate"] = ngram_df.duplicated(subset="starting_index", keep='last')

    ngram_df = ngram_df.query('is_duplicate == False')

    for _, row in ngram_df.iterrows():
        for i in range(row.ngram_len):
            if i==0:
                tag = "<B>"
            else:
                tag = "<I>"
            df.at[row.starting_index+i,"tag"] = tag
    
    df_flat = list(zip(df["token"],df["tag"]))

    t = " ".join([item for t in df_flat for item in t if type(item) == str and item != "O"])

    return t
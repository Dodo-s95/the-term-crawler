import spacy
import csv
import pandas as pd

from spacy.lang.char_classes import ALPHA, ALPHA_LOWER, ALPHA_UPPER
from spacy.lang.char_classes import CONCAT_QUOTES, LIST_ELLIPSES, LIST_ICONS
from spacy.util import compile_infix_regex

nlp = spacy.load("en_core_web_sm")

# modify tokenizer infix patterns for avoiding hyphenated words being split (several terms are hyphenated)

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

# reads terms

def read_tsv(link):
    with open(link, "r", encoding="utf-8") as tsvfile:
        reader = csv.reader(tsvfile, delimiter="\t")
        next(reader) # skip header
        return {row[2].split(": ")[1] for row in reader}
        #return [pd.DataFrame(row[2].split(": ")[1].split(" ")) for row in reader]

terms_lexicon = read_tsv("../swimming-terms_keep4k.tsv") # extracted terms

# open corpus, spacy it

with open("../corpus_txt/manuscript-maglischo-vol22.txt") as f: # corpus here
    doc = f.readlines()[0]
    doc = nlp(doc)

# creates df token by token with sentences split by \n

df = pd.DataFrame([item for sub in [[tok.text for tok in s]+["\n"] for s in doc.sents] for item in sub], columns=["token"])

# lemmatize, lowercase

df["lemma"] = [item for sub in [[token.lemma_.lower() if token.lemma_ != '-PRON-' else token.lower_ for token in s]+["\n"] for s in doc.sents] for item in sub]

# populate 3rd column with "O" tags

df["tag"] = ["O"]*len(df)

# # loops over substrings of len from 1 to longer term (i), for each term checks if substring matches with any of the terms

# terms_lens = reversed(range(1, max([len(t.split(" ")) for t in terms_lexicon])+1))

# b = 0
# e = 0

# for i in terms_lens:
#     print(i)
#     while b <= len(doc_lemma) - i:
#         for term in terms_lexicon:
#             substring = " ".join(doc_lemma[b:i+e])
#             if substring == term:
#                 if i == 1:
#                     doc_lemma[b:i+e] = None
#         b += 1
#         e += 1
#     b = 0
#     e = 0

#def sliding_window():


terms_lens = reversed(range(1, max([len(t.split(" ")) for t in terms_lexicon])+1))

b = 0
e = 0

for i in terms_lens:
    print(i)
    while b <= len(df) - i:
        for term in terms_lexicon:
            term = pd.DataFrame(term.split(" "))
            window = df["lemma"].iloc[b:e+i]
            print(window)
            if window.equals(term):
               print("OK")
        b += 1
        e += 1
    b = 0
    e = 0

# for term in terms_lexicon:
#     term = pd.DataFrame(term.split(" "))
#     if window.equals(term):
#         pass # put B I O
import numpy as np
def windows(d, w, t):
    r = np.arange(len(d))
    s = r[::t]
    z = list(zip(s, s + w))
    f = '{0[0]}:{0[1]}'.format
    g = lambda t: d.iloc[t[0]:t[1]]
    return pd.concat(map(g, z), keys=map(f, z))

wdf = windows(df, 3, 1)
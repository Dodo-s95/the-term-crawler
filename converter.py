import glob
from pdfminer.high_level import extract_text

for istr in glob.iglob("../corpus_pdf/*.pdf"):
    with open("../corpus_txt/{}.txt".format(istr.split("/")[-1].split(".")[0]), "w+", encoding="utf-8") as ostr:
        text = extract_text(istr)
        ostr.write(" ".join(text.split()))
import requests, os, time, random
from bs4 import BeautifulSoup
import urllib.request

# create folder stucture for the corpora needed for the whole project

root_path = '../corpora/'
folders = ['corpus_pdf','corpus_txt','corpus_bio']
for folder in folders:
    os.makedirs(os.path.join(root_path, folder), exist_ok=True)

print("Directory structure created.")

# extract PDF files

base_url = "https://swimmingcoach.org/journal/"
archive = base_url + "archive.php"

r = requests.get(archive).text
soup = BeautifulSoup(r, "html.parser")

journals = [li.find("a")["href"].split("/")[-1] for div in soup.find_all("div", id="content_right") for li in div.find_all("li") if li.find("a").get_text() in ["(Manuscript)", "(Coaching Applications)"]]

for journal in journals:
    journal_url = base_url + journal
    try:
        urllib.request.urlretrieve(journal_url, "../corpora/corpus_pdf/{}".format(journal))
        time.sleep(random.random.uniform(0.5, 1.5))
    except:
        pass

print("PDF extraction complete.")
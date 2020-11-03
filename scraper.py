import requests
from bs4 import BeautifulSoup
import urllib.request

base_url = "https://swimmingcoach.org/journal/"
archive = base_url + "archive.php"

r = requests.get(archive).text
soup = BeautifulSoup(r, "html.parser")

journals = [li.find("a")["href"].split("/")[-1] for div in soup.find_all("div", id="content_right") for li in div.find_all("li") if li.find("a").get_text() in ["(Manuscript)", "(Coaching Applications)"]]

for journal in journals:
    journal_url = base_url + journal
    try:
        urllib.request.urlretrieve(journal_url, "../corpus_pdf/{}".format(journal))
    except:
        pass
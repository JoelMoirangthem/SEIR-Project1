import sys
import requests
from bs4 import BeautifulSoup


def extractWebpage(websiteLink):
    header = {
        'User-Agent': 'Mozilla'
    }

   
    if not websiteLink.startswith("http://") and not websiteLink.startswith("https://"):
        websiteLink = "https://" + websiteLink

    outputData = requests.get(websiteLink, headers=header)
    return outputData.text


def webPageData(webpage):

    soup = BeautifulSoup(webpage, "html.parser")

    title = ""
    if soup.title:
        title = soup.title.string

    body = ""
    if soup.body:
        body = soup.body.get_text(" ", strip=True)

    links = []

    for anchor_tag in soup.find_all("a"):
        link = anchor_tag.get("href")
        if link:
            links.append(link)

    return title, body, links


url = sys.argv[1]

html = extractWebpage(url)
title, body, links = webPageData(html)

print(title)
print(body)

for link in links:
    print(link)
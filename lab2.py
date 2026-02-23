import sys
import requests
from bs4 import BeautifulSoup

def extractWebpage(websiteLink):
    header = {
        'User-Agent' : 'Mozilla'
    }
    outputData = requests.get(websiteLink,headers = header)
    if outputData.status_code == 200:
        return outputData.text
    else:
        return ""

def webPageData(webpage):

    soup = BeautifulSoup(webpage,"html.parser") 
    
    title = ""
    if(soup.title):
        title = soup.title.string
        

    
    body = soup.body.get_text(" ", strip=True)
    

    links = [] 
   
    for anchor_tag in soup.find_all("a"):
        link = anchor_tag.get("href")
        if link:
            links.append(link)
    return title , body , links

def wordFrequency(text):
   
    text = text.lower()
    
    cleanWords = "" 
    
    
    for char in text:
        if char.isalnum():
            cleanWords += char
        else:
            cleanWords += " "
    wordsList = cleanWords.split()
    freqWord = {}
    for word in wordsList:
        if word in freqWord:
            freqWord[word] += 1
        else:
            freqWord[word] = 1
    return freqWord

p = 53
m = 2**64
def rolling_hash(word):
    hashVal = 0
    i = 1
    for letter in word:
        hashVal += (ord(letter) * i)
        i *= p
    
    return hashVal % m

def compute_simhash(freq):

    vector = [0 for _ in range(64)]

    for word, count in freq.items():
        h = rolling_hash(word)

        for i in range(64):
            bit = (h >> i) & 1

            if bit:
                vector[i] += count
            else:
                vector[i] -= count

    result = 0

    for i in range(64):
        if vector[i] > 0:
            result |= (1 << i)
    #  3 4 1 0 -8 -7 5 6
    # 1 1 1 1 0 0  1 1
    
    return result

def common_bits(f1, f2):
    bitChange = f1 ^ f2
    count = 0
    while bitChange:
        count += bitChange & 1
        bitChange >>= 1
    return 64 - count

if len(sys.argv) < 3:
    print("Usage: python lab2.py <URL1> <URL2>")
else:
    url1 = sys.argv[1]
    url2 = sys.argv[2]

    html1 = extractWebpage(url1)
    if html1:
        title1, body1, links1 = webPageData(html1)
        freq1 = wordFrequency(body1)
        h1 = compute_simhash(freq1)
    else:
        print("Error fetching first URL")
        h1 = 0

    html2 = extractWebpage(url2)
    if html2:
        title2, body2, links2 = webPageData(html2)
        freq2 = wordFrequency(body2)
        h2 = compute_simhash(freq2)
    else:
        print("Error fetching second URL")
        h2 = 0

    result = common_bits(h1, h2)
    print(result)
from bs4 import BeautifulSoup
import requests

def rt_scrap(player):   

    # search player useing statbunker search engine
    url = "https://www.statbunker.com/usual/search?action=Find&search="+str(player)
    req = requests.get(url)
    src = req.content

    soup = BeautifulSoup(src, 'html.parser')

    result = soup.find_all("a", {"class": "linkGreen"})

    # go to the first result's page
    url = "https://www.statbunker.com"+str(result[0]['href'])
    req = requests.get(url)
    src = req.content

    soup = BeautifulSoup(src, 'html.parser')

    result = soup.find("caption", {"class": "genericTitle"})
    name = result.find('h1').text

    result = soup.find_all("table", {"class": "genericTable table hidden all_time"})

    for res in result:

        res = res.find_all('td')

    return name , res[1].text, res[2].text, res[3].text, res[4].text, res[5].text, res[6].text, res[7].text, res[8].text
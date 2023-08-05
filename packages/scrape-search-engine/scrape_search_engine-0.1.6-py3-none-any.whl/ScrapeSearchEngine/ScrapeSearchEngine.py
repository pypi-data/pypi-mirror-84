import requests
from bs4 import BeautifulSoup

#Github: https://github.com/sujitmandal
#This programe is create by Sujit Mandal
"""
Github: https://github.com/sujitmandal
Pypi : https://pypi.org/user/sujitmandal/
LinkedIn : https://www.linkedin.com/in/sujit-mandal-91215013a/
"""

#search on google "my user agent"
#USER_AGENT = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36')
#search = ('')

userAgent = ('') #my user agent
search = ('') #Enter Anything for Search

def Google(search, userAgent):
    URL = ('https://google.com/search?q=' + search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        results = []
    
        for i in soup.find_all('div', {'class' : 'yuRUbf'}):
            link = i.find_all('a')
            links = link[0]['href']
            results.append(links)
    return(results)

def Duckduckgo(search , userAgent):
    URL = ('https://duckduckgo.com/html/?q=' + search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        results = []

        for i in soup.find_all('a', attrs={'class':'result__a'}):
            links = i['href']
            results.append(links)
    return(results)

def Givewater(search, userAgent):
    URL = ('https://search.givewater.com/serp?q='+search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        results = []

        for i in soup.find_all('div', {'class' : 'web-bing__result'}):
            link = i.find_all('a')
            links = link[0]['href']
            results.append(links)
    return(results)


def Ecosia(search, userAgent):
    URL = ('https://www.ecosia.org/search?q='+search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        results = []

        for i in soup.find_all('div', {'class' : 'result-firstline-container'}):
            link = i.find_all('a')
            links = link[0]['href']
            results.append(links)
    return(results)

def Bing(search, userAgent):
    URL = ('https://www.bing.com/search?q='+search)
    headers = {'user-agent' : userAgent}
    request = requests.get(URL, headers=headers)

    if request.status_code == 200:
        soup = BeautifulSoup(request.content, "html.parser")
        results = []
    
        for i in soup.find_all('li', {'class' : 'b_algo'}):
            link = i.find_all('a')
            links = link[0]['href']
            results.append(links)
    return(results)

def Yahoo(search, userAgent):
    URL = ('https://search.yahoo.com/search?q=' + search)
    request = requests.get(URL)

    if request.status_code == 200:
        soup = BeautifulSoup(request.content, 'html.parser')
        results = []
    
        for i in soup.find_all(attrs={"class": "ac-algo fz-l ac-21th lh-24"}):
            link = i.get('href')
            results.append(link)

    return(results)

if __name__ == "__main__":
    Bing(search, userAgent)
    Yahoo(search, userAgent)
    Google(search, userAgent)
    Ecosia(search, userAgent)
    Givewater(search, userAgent)
    Duckduckgo(search, userAgent)
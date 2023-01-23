import os, sys, bs4, requests, webbrowser, re

urlList = []
layerAdded = {}
depth = 3 # how many "layers" before stopping

def urlLister(url,depth):
    if depth == 0:
        return
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    for links in soup.find_all('a',attrs={'href': re.compile("^http://")}):
        link = links.get('href')
        if link not in urlList and type(link) == str:
            urlList.append(link)
            layerAdded.update({link:depth})
    for url in urlList:
        if layerAdded.get(url) == depth:
            urlLister(url,depth-1)
        
quit = False

while not quit:
    url = input("Enter a url: ")
    urlLister(url,depth)

    for url in urlList:
        print(url)


    exitprogram = input("Exit? Y/N?")
    if exitprogram.lower() == 'y':
        quit = True

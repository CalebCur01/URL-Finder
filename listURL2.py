import os, sys, bs4, requests, webbrowser, re

urlList = []
depth = 1 # how many "layers" before stopping

def urlLister(url,depth):
    if depth == 0:
        return
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    for links in soup.find_all('a',attrs={'href': re.compile("^http://")}):
        link = links.get('href')
        if link not in urlList and type(link) == str:
            print(url)
            urlList.append(link)
    for url in urlList:
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

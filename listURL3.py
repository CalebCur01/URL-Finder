import os, sys, bs4, requests, webbrowser, re, time

urlList = [] #list of website links
layerAdded = {} #keeps track of what "layer" each link was added
depth = 3 # how many "layers" before stopping
maximum = 8 #Set a limit of links to discover before stopping

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
            print("Website link found! - {} - Layers remaining: {}".format(link,depth-1))
            if len(urlList) >= maximum:
                print("Limit reached! Quitting early!")
                return
    for url in urlList:
        if layerAdded.get(url) == depth:
            urlLister(url,depth-1)
        
quit = False

while not quit:
    website = input("Enter a url: ")
    start = time.perf_counter()
    urlLister(website,depth)
    stop = time.perf_counter()

    
    print("\nStarting from {}, found {} links in {} seconds.".format(website,len(urlList),stop-start))

    exitprogram = input("Exit? Y/N?")
    if exitprogram.lower() == 'y':
        quit = True

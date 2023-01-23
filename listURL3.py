import os, sys, bs4, requests, webbrowser, re, time

urlList = [] #list of website links
layerAdded = {} #keeps track of what "layer" each link was added
depth = 2 # how many "layers" before stopping
maximum = 300 #Set a limit of links to discover before stopping


def urlLister(url,depth):
    if depth == 0:
        return
    if len(urlList) >= maximum:
        return
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    for links in soup.find_all('a',attrs={'href': re.compile("^http://|^https://")}):
        link = links.get('href')
        if link not in urlList and type(link) == str:
            urlList.append(link)
            layerAdded.update({link:depth})
            print("Website link found! - {} - {}".format(link,len(urlList)))
            if len(urlList) >= maximum:
                print("\nLimit reached! Quitting early!")
                return
    for url in urlList:
        if layerAdded.get(url) <= depth:
            urlLister(url,depth-1)
        
quit = False

while not quit:
    try:
        website = input("Enter a url: ")
        start = time.perf_counter()
        urlLister(website,depth)
        stop = time.perf_counter()

        
        print(f"\nStarting from {website}, found {len(urlList)} links in {stop-start:0.2f} seconds.")
    except:
        print("Process failed! Please enter a website!")

    exitprogram = input("Exit? Y/N?")
    if exitprogram.lower() == 'y':
        quit = True
    else:
        urlList.clear()

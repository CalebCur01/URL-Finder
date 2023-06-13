import os, sys, bs4, requests, webbrowser, re, time, json
from pathlib import Path
from visualizer import visualize 

urlList = [] #list of website links
searched = {} #This will keep track of which webpages have already been searched before
layerAdded = {} #keeps track of what "layer" each link was added
parentList = {} #for keeping track of which link came from which website
depth = 4 # how many "layers" before stopping
maximum = 250 #Set a limit of links to discover before stopping




def urlLister(url,depth):
    alreadySearched = searched.setdefault(url,False)

    if depth == 0:
        return
    if len(urlList) >= maximum:
        return
    if alreadySearched:
        return
    
    print("Searching %s for links..."%url)
    req = requests.get(url)
    soup = bs4.BeautifulSoup(req.text,"html.parser")
    searched.update({url:True})
    for links in soup.find_all('a',attrs={'href': re.compile("^http://|^https://")}):
        link = links.get('href')
        if link not in urlList and type(link) == str:
            urlList.append(link)
            parentList.update({link:url})
            layerAdded.update({link:depth})

            print("Website link found! - {} - {}".format(link,len(urlList)))

            if len(urlList) >= maximum:
                print("\nLimit reached! Quitting early!")
                return

    for url in urlList:
        if layerAdded.get(url) == depth:
            urlLister(url,depth-1)
            
            
        
quit = False

while not quit:
    urlList.clear()
    parentList.clear()
    searched.clear()
    try:
        website = input("Enter a url: ")
        maximum = int(input("Enter max number of links: "))
        depth = int(input("Enter maximum depth: "))

        start = time.perf_counter()
        urlLister(website,depth)
        stop = time.perf_counter()

        
        print(f"\nStarting from {website}, found {len(urlList)} links in {stop-start:0.2f} seconds.")
        with open("urls.txt",'w') as file:
            file.write(json.dumps(parentList))
        visualize()
        
        

        
    except:
        print("Process failed!")


    exitprogram = input("Exit? Y/N")
    if exitprogram.lower() == 'y':
        quit = True
        

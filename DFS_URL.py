#DFS_URL - Performs depth first search for webpages
import os, sys, bs4, requests, webbrowser, re, time, csv
from pathlib import Path
from csv_to_graph import visualize 

data_dict = {} #each key is a parent website, each value is a list of links found on that website
max_parents = 0 # how many parents before stopping
max_children = 0 #how many children before stopping
child_count = 0     #keeps count of how many children we have added (includes duplicates)



def urlLister(parent, max_parents, max_children):
    """Search for webpages depth first"""
    global child_count
    #Skip webpages that have already been visited
    if parent in data_dict:
        return   

    data_dict.update({parent:[]})

    print(f"Searching {parent} for links...")
    req = requests.get(parent)
    soup = bs4.BeautifulSoup(req.text,"html.parser")

    for children in soup.find_all('a',attrs={'href': re.compile("^http://|^https://")}):
        child = children.get('href')
        if type(child) == str:
            data_dict[parent].append(child)
            child_count += 1

            print("Website link found! - {} - {}".format(child,child_count))

            if child_count >= max_children or len(data_dict) >= max_parents:
                print("\nLimit reached! Quitting early!")
                return 'QUIT'

    for child in data_dict[parent]:
        result = urlLister(child,max_parents,max_children)
        if result == 'QUIT':
            return 'QUIT'

def save_csv(data,filename):
    """save dictionary as csv"""
    with open(f'{filename}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #Write the header
        writer.writerow(["source", "target"])
        #Loop through the dictionary
        for parent, children in data.items():
            #Loop through the list of values
            for child in children:
                #Write the key and value to the CSV
                writer.writerow([parent, child])
                    


quit = False

while not quit:
    data_dict.clear()
    child_count = 0
    parent_count = 0
    try:
        website = input("Enter a url: ")
        max_parents = int(input("Enter max number of parent websites: "))
        max_children = int(input("Enter max number of child websites: "))

        start = time.perf_counter()
        urlLister(website,max_parents,max_children)
        stop = time.perf_counter()

        print(f"\nStarting from {website}, found {child_count} links in {stop-start:0.2f} seconds.")

        save_csv(data_dict,"Durls")
        visualize("Durls")        

    except Exception as e:
        print("Process failed!")
        print(e)

    exitprogram = input("Exit? Y/N")
    if exitprogram.lower() == 'y':
        quit = True
        

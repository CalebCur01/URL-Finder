import os, sys, bs4, requests, webbrowser, re, time, csv
from urllib.parse import urlparse
from collections import deque
from pathlib import Path
from csv_to_graph import visualize 

nodes = {} #each key is a parent website, each value is a list of links found on that website
max_parents = 0 # how many parents before stopping
max_children = 0 #how many children before stopping
child_count = 0 #how many children we have added (includes duplicates)


def normalize_url(url):
    parsed = urlparse(url)
    scheme = parsed.scheme or 'http'
    netloc = parsed.netloc or parsed.path
    path = parsed.path if parsed.netloc else ''
    if netloc.startswith('www.'):
        netloc = netloc[4:]
    if netloc.endswith('/'):
        netloc = netloc[:-1]
    if path.endswith('/'):
        path = path[:-1]
    return f'{scheme}://{netloc}{path}'

def urlLister(parent, max_parents, max_children):
    """Search for webpages breadth first """
    global child_count

    parent = normalize_url(parent)

    queue = deque([(parent)])

    while queue:
        parent = queue.popleft()

        if parent in nodes:
            continue

        nodes[parent] = []

        try:
            print(f"Searching {parent} for links...")
            req = requests.get(parent)
            soup = bs4.BeautifulSoup(req.text,"html.parser")

            for children in soup.find_all('a',attrs={'href': re.compile("^http://|^https://")}):
                child = children.get('href')

                if type(child) == str:
                    child = normalize_url(child)
                    nodes[parent].append(child)
                    queue.append(child)
                    child_count += 1

                    print("Website link found! - {} - {}".format(child,child_count))

                    if child_count >= max_children or len(nodes) >= max_parents:
                        print("\nLimit reached!")
                        return

        except Exception as e:
            print(f"Failed to get links from {parent}: {e}")
            continue

def save_csv(data,filename):
    """save dictionary as csv"""
    with open(f'{filename}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #Write the header
        writer.writerow(['source', 'target'])
        #Loop through the dictionary
        for parent, children in data.items():
            #Loop through the list of values
            for child in children:
                #Write the key and value to the CSV
                writer.writerow([parent, child])
            


quit = False

while not quit:
    nodes.clear()
    child_count = 0
    parent_count = 0
    try:
        website = input("Enter a url: ")
        max_parents = int(input("Enter max number of parent websites: "))
        max_children = int(input("Enter max number of child websites: "))

        start = time.perf_counter()
        urlLister(website, max_parents,max_children)
        stop = time.perf_counter()

        print(f"\nStarting from {website}, found {child_count} links in {stop-start:0.2f} seconds.")

        save_csv(nodes,"Burls")
        visualize("Burls")      

    except Exception as e:
        print("Process failed!")
        print(e)

    exitprogram = input("Exit? Y/N")
    if exitprogram.lower() == 'y':
        quit = True

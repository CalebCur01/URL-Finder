#listURL - find all links on webpage
import os, sys, bs4, requests, webbrowser, re

url = input("Enter a url: ")
req = requests.get(url)
soup = bs4.BeautifulSoup(req.text, "html.parser")

for link in soup.find_all('a'):
    print(link.get('href'))



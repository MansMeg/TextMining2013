'''
Created on Apr 27, 2013

A simple parallelized web crawler that indexes Google Play and
App Brain (not fully implemented yet)

It does not respect robots.txt, but tries to play nice by having
a random delay of a few seconds so as not to overload sites with
requests

@author: Leif Jonsson & Mans Magnusson
'''

import Queue
import os
from urllib import urlopen
import multiprocessing
import sys
import signal
import time
import random
import re
import nltk
import string
import threading
from HTMLParser import HTMLParser

# Change WD to be able to version control 
os.chdir("/Users/mansmagnusson/Desktop/Text Mining/Labs/TextMining2013/L4")

# Booleans to control running threads
link_finder_continue = True
downloader_continue  = True
running_threads      = []

# Blocking queue to store links we have found but not downloaded yet
link_queue = Queue.Queue()

# URLs to sites to Crawl
google_play = "https://play.google.com/"
app_brain   = "http://www.appbrain.com/"

# Text file where we store already downloaded files
# one URL per line
downloaded_links_fn = "dl_links.txt"

# Create the downloaded links file  if it does not exist
if not os.path.exists(downloaded_links_fn):
    open(downloaded_links_fn, 'a').close()
## M: Vad innebär "a" i detta sammanhang? Vad gör du här?

# Hash table with all the downloaded links we have
downloaded_links = {}
with open(downloaded_links_fn) as dls:
    for link in dls:
        downloaded_links[link.rstrip()] = True

print "Previously Downloaded Links are:"
for link in downloaded_links.keys():
    print "=>{0}".format(link)        

# How many links we have downloaded
urlcnt = 0

# Directory to save downloaded html in
file_savedir = "texts"

# Create the directory where we save the html 
# if it does not already exists
if not os.path.exists(file_savedir):
    os.makedirs(file_savedir)

def find_gp_categories_links(html):
    """
    Finds links to the different App category pages on Google Play
    """
    links = []
    for m in re.finditer('href="(/store/apps/category/[^"]+)"', html):
        #print '%02d-%02d: %s' % (m.start(), m.end(), m.group(1))
        links.append(m.group(1))
    return links

def find_gp_app_links(html):
    """
    Finds links to Apps on Google Play app collection pages
    """
    links = []
    for m in re.finditer('href="(/store/apps/details[^"]+)"', html):
        #print '%02d-%02d: %s' % (m.start(), m.end(), m.group(1))
        links.append(m.group(1))
    return links

def get_gp_text_description(html):
    """
    Given an Google Play Appp HTML page this method returns the description as text
    """
    m = re.search('<div id="doc-description-container"', html)
    desc_section_start = html[m.start():]
    m = re.search('</div>', desc_section_start)
    desc_section = desc_section_start[:m.start()]
    cleaned_desc = filter(lambda x: x in string.printable, desc_section)
    parser = HTMLParser()
    return parser.unescape(nltk.clean_html(cleaned_desc))

def write_downloaded_links():
    """
    Writes a text file with the links that are downloaded, so we keep fetching new pages every time
    """
    global downloaded_links_fn
    text_file = open(downloaded_links_fn,"w")
    for link in downloaded_links.items():
        text_file.write(link[0] + "\n")
    text_file.close()

def sim_download_link(url,save_dir):
    """
    Simulates downloading links
    """
    global downloaded_links
    if url in downloaded_links.keys(): return None
    m = re.search('\?id=([a-zA-Z0-9.]+)', url)
    unique_name = m.group(1)
    unique_name = unique_name.replace(".","_") + ".txt"
    print("Would download {0} and save it in '{1}' as {2}".format(url, save_dir, unique_name))
    downloaded_links[url] = True
    return unique_name
    
def download_link(url,save_dir):
    """
    Downloads an url and converts it to text, then saves it to the save folder.
    Returns the HTML or None if link is already downloaded. 
    Adds the link to the global list of downloaded links.
    """
    global downloaded_links
    global urlcnt
    if url in downloaded_links.keys(): return None
    m = re.search('\?id=([a-zA-Z0-9.]+)', url)
    unique_name = m.group(1)
    unique_name = unique_name.replace(".","_")
    text_name = unique_name + ".txt"
    html = urlopen(url).read()
    text_file = open(save_dir + "/{0}".format(text_name),"w")
    urlcnt += 1
    text_version = get_gp_text_description(html)
    text_file.write(text_version)
    text_file.close()
    downloaded_links[url] = True
    print("Downloaded {0} and saved it in '{1}' as {2}".format(url, save_dir, unique_name))
    return html

def gp_link_finder(url):
    """
    The main Google Play link finder. Downloads the Google Play start page
    then finds the category pages, and downloads each category page. 
    For each category page finds all App links on that page.
    """
    print("Starting to find links on Google Play ({0})...".format(url))
    # Download google Play start Page
    start_page = urlopen(url + "/store").read()
    global link_queue
    global link_finder_continue
    # Find the App category pages
    link_pages = find_gp_categories_links(start_page)
    # For each category page, find all App Links on that page
    while link_finder_continue:
        for link_page_lnk in link_pages:
            # Download the category page
            print("Fetching link page {0}".format(url + link_page_lnk))
            link_page = urlopen(url + link_page_lnk).read()
            # Find the app links
            app_links = find_gp_app_links(link_page)
            # Add the link in the queue for the link downloader
            didadd = False
            for link in app_links:
                if not (url+link) in downloaded_links.keys():
                    link_queue.put(url + link)
                    didadd = True
                    print("Added {0} to download queue...".format(url + link))
            if didadd:
                # Sleep for a while to not overload site
                sleep_time = random.randint(20,30)
                print("Link finder sleeping for {0} seconds...".format(sleep_time))
                time.sleep(sleep_time)
    print("Exiting link finding...")

def ab_link_finder(url):
    print("Starting to find links on App Brain...")
    global link_queue
    global link_finder_continue
    while link_finder_continue:
        time.sleep(random.randint(1,10))
        print "Fake looking for link on App Brain..."
    print("Exiting link finding on App Brain...")

def downloader(download_fun):
    global link_queue
    global downloader_continue
    global file_savedir
    while downloader_continue:
        link = link_queue.get()
        result = download_fun(link, file_savedir)
        link_queue.task_done()
        # Only sleep if we actuallt accessed the website
        if not result is None:
            # Sleep for a while to not overload site
            sleep_time = random.randint(1,10)
            print("Downloader thread {0} is sleeping for {1} seconds...".format(threading.current_thread().getName(), sleep_time))
            time.sleep(sleep_time)

# If we need to do some cleanup
def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        global link_finder_continue
        link_finder_continue = False
        global downloader_continue
        downloader_continue  = False
        write_downloaded_links()
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print 'Pressing Ctrl+C will cleanly abort program...'

print("Starting Google Play link finder...")
# Create the threads to find links
## Vad menas med Threads?
gplf = threading.Thread(target=gp_link_finder, args=(google_play,)) # UUUUGly, the last comma is needed in args list
gplf.daemon = True
#ablf = Thread(target=ab_link_finder, args(app_brain,))
#ablf.daemon = True

gplf.start()
#ablf.start()
        
# How many downloader threads we want to run
downloader_threads = max(multiprocessing.cpu_count() / 2, 1)
print("Using {0} downloader threads...".format(downloader_threads))

for i in range(downloader_threads):
    print("Starting downloader thread...")
    t = threading.Thread(target=downloader, args=(download_link,))
    t.daemon = True
    t.start()

# Loop until we have downloaded 1000 links
while urlcnt < 1000:
    time.sleep(1)
    
link_queue.join()       # block until all tasks are done
write_downloaded_links()
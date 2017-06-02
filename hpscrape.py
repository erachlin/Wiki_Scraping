import bs4
import re
import csv

import urllib 
from urllib import urlopen as uReq
from bs4 import BeautifulSoup as soup

base_url = 'http://harrypotter.wikia.com'
my_url = 'http://harrypotter.wikia.com/wiki/Category:Harry_Potter_universe'
'''
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
'''


def page_crawler(urls, visited):
	
	if urls[0] not in visited:
		while len(urls) > 0:
			try:
				#htmltext = urllib.urlopen(page_html).read()
				uClient = uReq(urls[0])
				page_html = uClient.read()
				uClient.close()
				scrape_links(page_html, urls)
			except:
				print urls[0]
			
			visited.append(urls[0])
			print visited[-1]
			urls.pop(0)
			
	else:
		urls.pop(0)
		if len(urls) != 0:
			print len(urls)
			page_crawler(urls)			
			
	

#html parsing
def scrape_links(page_html, urls):
	subcategories = []
	pages = []

	page_soup = soup(page_html, "html.parser")
	subcategory_data = page_soup.findAll("a", {"class":"CategoryTreeLabel"})
	for subcategory in subcategory_data:
		subcategories.append(base_url + subcategory["href"])
		urls.append(base_url + subcategory["href"])
	print len(urls)
	cat_strings = str(subcategories)
	pagedata = page_soup.findAll("div", {"id":"mw-pages"})
	text = str(pagedata)
	pattern = '<a href="(/wiki/[^"]+)" title="([^"]+)"' #'>([^<]+)'
	matches = re.findall(pattern, text)
	for hit in matches:
		pages.append(base_url + hit[0])

	pagestrings = str(pages)
	write_file(page_html, subcategories, pages, files_written)



def write_file(page_html, subcategories, pages, files_written):
	#if "Category:" not in str(page_html):
		#return
	filename =  'test' + str(files_written) + ".csv"
	f = open(filename, "w")
	headers = "Subcategories\n"
	f.write(headers)
	for cat in subcategories:
		f.write(cat + "\n")
		urls.append(cat)
	print "csv writing halfway complete"	
	f.write("Sub-Pages" + "\n")
	for page in pages:
		f.write(page + "\n")
	files_written += 1
	f.close()
	
	return


def main():
	urls = [my_url] # stack of urls to scrape
	visited = [] # historic record of urls
	files_written = 0

	'''
	print 'Welcome to the Wikipedia Web Scraper, Version 1.0'
	print 'Please enter your wikipedia categories URL:'
	'''
	#user enters url to be scraped
	
	page_crawler(urls, visited)



if __name__ == '__main__':
	
	print 'starting up'
	main()

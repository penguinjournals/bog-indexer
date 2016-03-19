# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re

#url = 'http://localhost:8000/castell/bog/2016/'
url = 'https://ssl4.gipuzkoa.net/castell/bog/2016/'
def retrieve_url_content(url):
    req = None
    req = requests.get(url)
    return req

def crawl_links(req):
    html = BeautifulSoup(req.text)
    links = html.find_all('a')
    for key,link in enumerate(links):
        if '[To Parent Directory]' != link.get_text():
            link_url = "https://ssl4.gipuzkoa.net"+link.get('href')
            raw_input("Complete url: "+link_url+" Press enter to continue")
            scrap(link_url)
        else:
            print "Skipped: "+link.get_text()

def scrap(url):
    req = retrieve_url_content(url)
    crawl_links(req)

def crawl_links_from_url(url):
    req = retrieve_url_content(url)
    html = BeautifulSoup(req.text)
    links = html.find_all('a')
    crawled_links = []
    for key,link in enumerate(links):
        if '[To Parent Directory]' != link.get_text():
            link_url = "https://ssl4.gipuzkoa.net"+link.get('href')
            crawled_links.append(link_url)
        else:
            print "Skipped: "+link.get_text()
    return crawled_links

def parse_article(url):
    req = retrieve_url_content(url)
    html = BeautifulSoup(req.text)
    fecha = html.find(id="fecha").get_text()
    nro_seccion = html.find(id="nro_seccion").get_text()
    desc_seccion = html.find(id="desc_seccion").get_text()
    print fecha

def parse_bog_contents(bog_contents):
    for bog_content in bog_contents:
        article_name = bog_content.rsplit('/', 1)[-1]
        pattern = re.compile("^c[0-9]*\.htm",re.IGNORECASE)
        if pattern.match(article_name):
            parse_article(bog_content)

def scrap_bog_contents(bog_links):
    for bog in bog_links:
        bog_contents = crawl_links_from_url(bog)
        parse_bog_contents(bog_contents)

def scrap_monthly_bogs(monthly_link):
    bog_links = crawl_links_from_url(monthly_link)
    scrap_bog_contents(bog_links)

if __name__ == "__main__":
    for year in range (2016,2017):
        for month in range (1,13):
            url = "https://ssl4.gipuzkoa.net/castell/bog/%d/%02d" % (year,month)
            scrap_monthly_bogs(url)
import requests
from googlesearch import search
import logging
import re
from bs4 import BeautifulSoup
import sys
from functools import partial


class Crawler:
  def __init__(self, search_keyword='',starting_url='',num=30):
    self.starting_url=starting_url
    self.search_keyword=search_keyword
    self.visited_links=set()
    self.results_no=num
    self.make_http=lambda x,y: y if y.startswith('http') or y.startswith('https') else x+'/'+y
    self.filter_text=lambda x:'wiki' not in x.lower() and 'youtube' not in x.lower()
    self.is_http=lambda x: x.lower().startswith('http') or x.lower().startswith('https')
  def get_search_links(self,keyword=''):
    if(len(keyword)==0):
      raise Exception('Search keyword cannot be empty')
    return search(query=keyword,tld='co.in',lang='en',num=self.results_no,stop=self.results_no)

  def _crawl(self, link,depth):
    '''
    Crawls the site and gets the info recursively    
    '''
    
    if depth==0:
      return 
    info,embedded_links=self.extract_info(link) # Both of this are generators
    print('\n'.join(line for line in info if len(line)>1))
    
    self.visited_links.add(link)
    for _link in filter(self.filter_text,embedded_links):
      if _link not in self.visited_links:
        self._crawl(_link,depth-1)
    
    

  def extract_info(self, link):
    
    try:
      response=requests.get(link)
      soup=BeautifulSoup(response.content,'html.parser')
      embedded_links=map(partial(self.make_http,link),[link.get('href') for link in soup.find_all("a") if link.get('href')!=None])
      for script in  soup(['script','style']):
        script.extract()
      lines=(line.strip() for line in soup.get_text().splitlines())
      return lines,embedded_links  
    except Exception as e:
      print(e)
    
          

  
  
  def __call__(self,keyword='',depth=1,starting_url=''):
    '''
    This should first get all the links from google. 
    For each item in that list crawl that website to a specific depth 
    A depth of 2 would mean a dfs of level 2 

    '''
    if len(starting_url)<0:

      self.starting_url=filter(self.filter_text,self.get_search_links(keyword))
      for i,link in enumerate(self.starting_url):
        print('Currently crawling {0}->{1}'.format(i,link))
        self._crawl(link,depth)
    else:
      self._crawl(starting_url,depth)  


if __name__=='__main__':

  logging.basicConfig(level=logging.DEBUG)
  crawler=Crawler()
  crawler(starting_url="https://www.indiatoday.in/")


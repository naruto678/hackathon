import json
import requests
from confluence.client import Confluence
from confluence.models.content import ContentType, ContentBody
import logging
access_token = "NzU1MjEzMzk0ODMzOhlMpsqwfeLi6BCNU75aR14GFCIP"
test_title = 'IntelliJ and CLion Setup for Impala Development'

expand_list =  ["space","body.view",'history' "version", "container", "children", "metadata", "extensions"]

def main(): 
    with Confluence('https://cwiki.apache.org/confluence', ('codemathison', 'Ricky123@')) as c:
        spaces = [space for space in c.get_spaces(expand = expand_list)]
        print(spaces.key)

            
"""        
        content = c.get_content(title = test_title, expand =expand_list)
        for con in content: 
            print(con.body.view)
            content_id = con.id
            child_content = c.get_child_pages(content_id, expand = expand_list)
            for child_con in child_content:
                print(child_con.body.view)
                print(child_con)
"""
class Crawler: 
    def __init__(self, page_title = None, space_key = None): 
        self.page_title = page_title
        self.space_key = space_key
    def __call__(self, *args, **kwargs):
        if self.page_title is None and self.space_key is None: 
            raise Exception("Both title and key cannot be None")
        if self.page_title is not None and self.space_key is not None: 
            self._crawl_with_both(self.space_key, self.page_title)
        elif self.page_title: 
            self._crawl_with_title(self.page_title)
        elif self.space_key: 
            self._crawl_with_space_key(self.space_key)
    
    def _crawl_with_space_key(self,space_key):
        pass 
    def _crawl_with_title(self, title): 
        pass 
    
    def _crawl_with_both(self, space_key , title): 
        pass 

if __name__ == '__main__': 
    main() 

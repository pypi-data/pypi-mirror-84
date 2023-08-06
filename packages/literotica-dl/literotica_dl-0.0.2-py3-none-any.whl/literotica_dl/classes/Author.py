import os

from html.parser import HTMLParser
from bs4 import BeautifulSoup as soupify
import requests

from .Story import Story

class Author(object):
    def __init__(self, uid):
        try:
            int(uid)
        except ValueError:
            raise ValueError("invalid author uid '%s'" %(uid))
        self.url = "https://literotica.com/stories/memberpage.php?uid=%s" %(uid)
        self.stories = []
        self.name = ""

    def fill_metadata(self):
        r = requests.get("%s&page=submissions" %(self.url))
        status = r.status_code // 100
        if status == 2:
            self.p = soupify(r.content, features="html.parser")
        elif status == 4:
            raise IOError("Client Error %s" %(r.status_code))
        elif status == 5:
            raise IOError("Server Error %s" %(r.status_code))
        else:
            raise IOError("Unidentified Error %s" %(r.status_code))

    def get_name(self):
        if not self.name:
            self.fill_metadata()

            self.name = self.p.find('a', {'class': 'contactheader'}).getText()
        return self.name

    def get_stories(self):
        if not self.stories:
            self.fill_metadata()
            
            # WARNING: hard coded class names
            tofind1, tofind2 = 'bb', 't-t84 bb nobck'
            self.stories = self.p.findAll('a', {'class': tofind1})
            self.stories += self.p.findAll('a', {'class': tofind2})
            self.stories = [x['href'][28:] for x in self.stories]
            # toFind1 and toFind2 can return duplicates.
            # convert to set and back to revmoe duplicates
            _ = set(self.stories)
            self.stories = list(_)
            self.stories = [Story(story_id) for story_id in self.stories]
        return self.stories

    def list_stories(self):
        if not self.stories:
            self.get_stories()
        for story in self.stories:
            print(story.get_title())

    def download_stories(self):
        try:
            os.mkdir(self.get_name())
        except OSError:
            pass # folder already exists
        os.chdir(self.get_name())
        self.get_stories()
        for story in self.stories:
            story.writeToDisk()

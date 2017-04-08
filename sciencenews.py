'''
Model for getting science news.
'''

import random
import socket
from multiprocessing.dummy import Pool as ThreadPool

import feedparser

socket.setdefaulttimeout(15)

rssurls = ['http://www.nature.com/nature/rdf/news/most-recent',
           'http://feeds.nature.com/NatureBiologicalSciencesResearch',
           'http://feeds.newscientist.com/life',
           'http://feeds.newscientist.com/humans',
           'http://feeds.newscientist.com/health',
           'https://rss.sciencedaily.com/top/health.xml',
           'https://rss.sciencedaily.com/mind_brain.xml',
           'https://rss.sciencedaily.com/living_well.xml',
           'https://rss.sciencedaily.com/plants_animals.xml',
           'https://www.eurekalert.org/rss/biology.xml',
           'http://feeds.biologynews.net/biologynews/headlines',
           'http://rss.medicalnewstoday.com/biology-biochemistry.xml',
           'http://www.sciencemag.org/rss/express.xml']

class ScienceNewsDB(object):
    def __init__(self, rssurls):
        self.rssurls = rssurls
        self.update_news()

    def update_news(self):
        self.news = retrieve_science_news(self.rssurls)

    def get_science_news(self, number):
        return random.sample(self.news, number)

def parse_rss(rssurl):
    rssfeeds = []
    feeds = feedparser.parse(rssurl)
    for post in feeds.entries[:15]:
        link = post.link
        if '?utm_campaign=RSS' in link:
            link = link[:link.index('?utm_campaign=RSS')]

        if len(post.summary) > 500:
            summary = post.summary[:400] + '...'
        else:
            summary = post.summary
        rssfeeds.append(post.title + ': \n' + summary + "\n" + link)
    print('Updated: ' + rssurl)
    return rssfeeds

def retrieve_science_news(rssurls):
    pool = ThreadPool(4)
    results = pool.map(parse_rss, rssurls)
    return [item for result in results for item in result]

db = ScienceNewsDB(rssurls)

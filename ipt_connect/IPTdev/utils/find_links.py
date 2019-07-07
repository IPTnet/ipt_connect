import lxml.html
from urllib2 import urlopen

head = 'http://127.0.0.1:8000'
http = 'http:'
dev =  '/IPTdev/'
urls = [
        'problems',
        'participants',
        'jurys',
        'tournament',
        'teams',
        'rounds',
        ]
tags = [
        '//a/@href', 
        '//link/@href', 
        '//img/@src', 
        '//svg/@xmlns', 
        ]

links_error = []
links_static = []
links_other = []

for ur in urls:
        r = urlopen(head + dev + ur)
        page = lxml.html.fromstring(r.read())
        for tag in tags:
                for link in page.xpath(tag):
                        if not link.startswith('http'):
                                if link.startswith('//'):
                                        links_other.append(http + link)
                                elif link.startswith('/static/'):
                                        links_static.append(link)
                                else: 
                                        links_other.append(head + link)
                        else: 
                                links_other.append(link)
unique_url = list(set(links_other)) # delete duplicate log lines

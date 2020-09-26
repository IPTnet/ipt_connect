import lxml.html
import requests
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
links_for_check_404_error = [
        'roundss',
        'rounds/-1/',
        'physics_fights/-1',
        'teams/Switzerlanda/',
        'teams/Italy/-1/',
        'problems/-1/',
        'participants/-1/',
        'jurys/-1/',
        ]

links_error = []
links_static = []
links_all = []

for ur in urls:
        r = urlopen(head + dev + ur)
        page = lxml.html.fromstring(r.read())
        for tag in tags:
                for link in page.xpath(tag):
                        if not link.startswith('http'):
                                if link.startswith('//'):
                                        links_all.append(http + link)
                                elif link.startswith('/static/'):
                                        links_static.append(link)
                                else: 
                                        links_all.append(head + link)
                        else: 
                                links_all.append(link)
unique_url = list(set(links_all)) # delete duplicate log lines

print 'Link checking ...'

for li in unique_url:
        status_code = requests.get(li).status_code
        if status_code != 200:
                links_error.append((li, status_code))

for li in links_for_check_404_error:
        link  = head + dev + li  
        status_code = requests.get(link).status_code
        if status_code != 404:
                links_error.append((link, status_code))

print 'Finished'
print 'Static files'
for i in set(links_static):
        print i
print 'Error links'
for i in links_error:
        print i
        
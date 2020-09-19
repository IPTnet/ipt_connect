import lxml.html
import requests
from urllib2 import urlopen
from find_links import *

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

links_error, links_static, unique_url = construct_links_list()

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
        
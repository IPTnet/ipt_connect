import os
import git
from urllib2 import urlopen
from find_links import unique_url

dir_path_repo = str(os.getcwd())
repo = git.Repo(dir_path_repo[:-24])
last_commit = str(repo.head.commit)[:7]
dir_path_dump = dir_path_repo[:-24] + 'dump/' + last_commit

if not os.path.exists(dir_path_dump):
        os.makedirs(dir_path_dump)
print 'Dump in {}'.format(dir_path_dump)

html_code  = [] 
add_url = []

for u in unique_url:
        add_url.append(u + '\n')
        add_url.append(urlopen(u).read())
        html_code.append(list(add_url))
        add_url = []

for page in range(len(html_code)):
        with open(dir_path_dump + '/page_' + str(page) + '.txt', 'w') as site:
            site.writelines(html_code[page])

import os
import git
import urllib
from urllib2 import urlopen
from find_links import construct_links_list

dir_path_repo = str(os.getcwd())
repo = git.Repo(dir_path_repo[:-24])
last_commit = str(repo.head.commit)[:7]
dir_path_dump = dir_path_repo[:-24] + 'dump/' + last_commit
unique_url = construct_links_list()[2]

if not os.path.exists(dir_path_dump):
        os.makedirs(dir_path_dump)
print 'Dump in {}'.format(dir_path_dump)

for u in unique_url:
	if u[:16] == "http://127.0.0.1": # Avoid external pages
		with open(dir_path_dump + '/' + urllib.quote(u).replace('/','_') + '.html', 'w') as page:
			page.writelines(urlopen(u).read())

# NOT WORKING

import git
import os
import sys
import difflib

hash_commit_1 = sys.argv[1]
hash_commit_2 = sys.argv[2]
dir_repo = os.getcwd()[:-24]
dir_path_diff = dir_repo + 'diff'
dir_path_dump = dir_repo + 'dump'
dir_path_diff_commit = dir_path_diff + '/diff_' + hash_commit_1 + '_' + hash_commit_2
dir_path_dump_commit_1 = dir_path_dump + '/' + hash_commit_1
dir_path_dump_commit_2 = dir_path_dump + '/' + hash_commit_2

list_files_1 = sorted(os.listdir(dir_path_dump_commit_1), key = lambda x: int(os.path.splitext(x.split('_')[1])[0]))
list_files_2 = sorted(os.listdir(dir_path_dump_commit_2), key = lambda x: int(os.path.splitext(x.split('_')[1])[0]))

change_in_txt = []

urls_dir_1 = []
urls_dir_2 = []

for f in list_files_1:
    with open(dir_path_dump_commit_1 + '/' + str(f), 'r') as page:
        url = page.readline()[:-2]
    urls_dir_1.append(url)

for f in list_files_2:
    with open(dir_path_dump_commit_2 + '/' + str(f), 'r') as page:
        url = page.readline()[:-2]
    urls_dir_2.append(url)

not_use_url = list(set(urls_dir_1) - set(urls_dir_2))
if not_use_url:
    not_use_url = [not_use_url[i] + '\n' for i in range(len(not_use_url))]
    not_use_url.insert(0, 'IN ONE OF COMMIT NOT FOUND URLS:\n')
    not_use_url.append('\n')

d = difflib.Differ()

for i, u in enumerate(urls_dir_1):
    if u in urls_dir_2:
        ind = urls_dir_2.index(u)
        with open(dir_path_dump_commit_1 + '/page_' + str(i) + '.txt', 'r') as page:
            old = page.read().split('\n')
        with open(dir_path_dump_commit_2 + '/page_' + str(ind) + '.txt', 'r') as page:
            new = page.read().split('\n')
        change = list(d.compare(old, new))
        delta_change = [l for l in change if l.startswith('+') or l.startswith('-') or l.startswith('?')]
        if delta_change:
            name_page = 'DIFFERENCE IN PAGE_' + str(i) + '\n'
            url_page = u + '\n'
            delta_change.insert(0, name_page)
            delta_change.insert(1, url_page)
            change_in_txt.append(delta_change)
            delta_change.append('\n')

diff_txt = []

for i in change_in_txt:
    diff_txt.append('\n'.join(i))

if not os.path.exists(dir_path_diff):
        os.mkdir(dir_path_diff)
print('Diff in {}'.format(dir_path_diff_commit))

with open(dir_path_diff_commit + '.txt', 'w') as page:
    page.writelines(not_use_url)
    page.writelines(diff_txt)        

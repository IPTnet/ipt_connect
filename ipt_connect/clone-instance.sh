#!/bin/bash

# Usage:
# ./clone-instance.sh IPTdev IPT2020
# IPTdev is the name of existing instance
# IPT2019 is the name of instance to be created


mv $2 $2.bak
cp -r $1 $2

git add $2
git commit -m "Copied $1 to $2 as is"

for f in `find $2 -type f` ; do
	#echo $f
	sed -i "s/$1/$2/g" $f
done;

#TODO: rename folders automatically, too!
mv $2/templates/$1 $2/templates/$2
mv $2/static/$1 $2/static/$2

git add $2
git commit -m "Replaced $1 with $2 in $2"

sed -ni "p; s/$1/$2/gp" ipt_connect/urls.py
sed -ni "p; s/$1/$2/gp" ipt_connect/settings.py

git add ipt_connect/urls.py ipt_connect/settings.py
git commit -m "Plugged $2 to the Django application index"

python manage.py makemigrations $2
python manage.py migrate

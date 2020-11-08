#!/bin/bash

# Usage:
# ./clone-instance.sh IPTdev IPTdev_pf2
# `IPTdev` is the name of existing instance
# `IPTdev_pf2` is the "shadow" of instance to be created

trash-put $2
ln -s $1 $2

trash-put $2/templates/$2
ln -s $1 $2/templates/$2
trash-put $2/static/$2
ln -s $1 $2/static/$2

git add $2
git add $1/templates/$2
git add $1/static/$2
git commit -m "Create $2 as a shadow copy of $1"


sed -ni "p; s/$1/$2/gp" ipt_connect/settings.py

git add ipt_connect/settings.py
git commit -m "Plug $2 to the Django application index"


cp db.sqlite3   db.sqlite3.shading-$1-to-$2.bak


python manage.py makemigrations $2

git add -f $2/migrations/$2/__init.py__
git commit -m "Create generic migrations for $2"


#python manage.py makemigrations $2
#python manage.py migrate

#git add db.sqlite3
#git commit -m "[DB] Perform generic DB migrations for $2"



./rename-app.sh db.sqlite3.shading-$1-to-$2.bak  $1  $2

./db-copy.sh    db.sqlite3.shading-$1-to-$2.bak  db.sqlite3  $2

git add db.sqlite3
git commit -m "[DB] Copy database tables from $1 to $2"

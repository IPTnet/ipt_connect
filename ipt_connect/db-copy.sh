#!/bin/bash

# Usage: ./db-copy.sh copy-from.sqlite3 copy-to.sqlite3 IPT_NAME

FROM=$1
TO=$2

#cp $TO "$TO.bak.$(date +%Y%m%d)"

NAME=$3

echo "Copying from $NAME from $FROM to $TO..."

TABLES=""

# Comment the following line if the instance has no SiteConfiguration
TABLES=$TABLES" siteconfiguration "

# Base abstractions - do not depend on other or on each other
TABLES=$TABLES" room problem team "

# Depend only on teams
TABLES=$TABLES" participant jury "

# Depend only on teams and problems
TABLES=$TABLES" apriorirejection supplementarymaterial "

# Rounds depend on rooms etc.
TABLES=$TABLES" round "

# Finally, everything dependent on rounds
TABLES=$TABLES" eternalrejection tacticalrejection jurygrade "


# Now we should construct the SQL query

QUERY="ATTACH DATABASE '$FROM' AS other; \n"
#QUERY=$QUERY $'\n'

echo "Start deleting old tables..."
for TABLE in $TABLES; do
	QUERY=$QUERY"DROP TABLE IF EXISTS main.${NAME}_${TABLE};\n"
done

QUERY=$QUERY" DETACH other; "

echo -e $QUERY

echo -e $QUERY | sqlite3 $TO

echo "Old tables have been deleted!"

for TABLE in $TABLES; do
	echo "${NAME}_${TABLE}"
	sqlite3 $FROM ".dump '${NAME}_${TABLE}'" | sqlite3 $TO
done

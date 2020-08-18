#!/bin/bash

# Usage: ./db-copy.sh copy-from.sqlite3 copy-to.sqlite3 IPT_NAME

# Theoretically, another name for a new tournament can be provided,
# but the application will probably fail
# (except some edge cases when only problems are filled)

FROM=$1
TO=$2

#cp $TO "$TO.bak.$(date +%Y%m%d)"

NAME=$3

NEWNAME=${4:-$NAME}

echo "Copying from  $FROM/$NAME  to  $TO/$NEWNAME ..."

TABLES=""

# Comment the following line if the instance has no SiteConfiguration
TABLES=$TABLES" siteconfiguration "

# Base abstractions - do not depend on other or on each other
TABLES=$TABLES" room problem team "

# Depend only on teams
TABLES=$TABLES" participant jury "

# Rounds depend on rooms etc.
TABLES=$TABLES" round "

# Finally, everything dependent on rounds
TABLES=$TABLES" eternalrejection tacticalrejection jurygrade "


# Now we should construct the SQL query

QUERY="ATTACH DATABASE '$FROM' AS other; \n"
#QUERY=$QUERY $'\n'

for TABLE in $TABLES; do
	QUERY=$QUERY"DELETE FROM main.${NEWNAME}_${TABLE};\n"
	QUERY=$QUERY"INSERT INTO main.${NEWNAME}_${TABLE} SELECT "
	QUERY=$QUERY"\x2A"
	QUERY=$QUERY" FROM other.${NAME}_${TABLE};\n";
done

QUERY=$QUERY" DETACH other; "

echo -e $QUERY

echo -e $QUERY | sqlite3 $TO


#!/bin/bash

# Usage: ./rename-app.sh db.sqlite3 OLDNAME NEWNAME

DB=$1
OLDNAME=$2
NEWNAME=$3

########################################################################

# Here we form the list of the tables to be renamed

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

########################################################################

# Now we should construct the SQL query

QUERY="UPDATE django_content_type SET app_label='$NEWNAME' WHERE app_label='$OLDNAME';\n"
QUERY=$QUERY"UPDATE django_migrations SET app='$NEWNAME' WHERE app='$OLDNAME';\n"


for TABLE in $TABLES; do
	QUERY=$QUERY"ALTER TABLE ${OLDNAME}_${TABLE} RENAME TO ${NEWNAME}_${TABLE};\n"
done


echo -e $QUERY

echo -e $QUERY | sqlite3 $DB

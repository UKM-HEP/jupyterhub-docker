#!/bin/bash

IFS="
"
diskdir="/disk01/jupyter"

for line in `cat jupyterhub/userlist`; do

    test -z "$line" && continue
    user=`echo $line | cut -f 1 -d' '`
    [ -d "$diskdir/$user" ] && continue
    echo "create directory for user $user : $diskdir/$user"
    mkdir $diskdir/$user
    chmod 775 $diskdir/$user
    chown :100 $diskdir/$user
    chmod g+s $diskdir/$user
    cp -r $diskdir/examples $diskdir/$user

    chmod 775 $diskdir/$user/examples
    chown :100 $diskdir/$user/examples
    chmod g+s $diskdir/$user/examples
done

#!/bin/sh

IFS="
"
for line in `cat userlist`; do
  test -z "$line" && continue
  user=`echo $line | cut -f 1 -d' '`
  echo "adding user $user"
  useradd -m -s /bin/bash $user
  mkdir /home/$user/examples
  touch /home/$user/examples/madafaka
  #cp -r /srv/ipython/examples /home/$user/examples
  chown -R $user /home/$user/examples
done

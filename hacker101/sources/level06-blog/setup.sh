#!/bin/bash
set -e

chgrp -R mysql /var/lib/mysql
service mysql start &
python setup.py
rm setup.py
export FLAGS='[]'

/usr/sbin/apache2ctl -D FOREGROUND
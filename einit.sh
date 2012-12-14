#!/usr/bin/env expect

# spawn rm sql/db.sqlite3
# expect eof

spawn ./manage.py syncdb
expect "(yes/no): "
send "yes\n"
expect ": "
send "admin\n"
expect "address: "
send "jknaperek@gmail.com\n"
expect ": "
send "a\n"
expect ": "
send "a\n"
expect eof

# spawn ./manage.py createinitialrevisions
# expect eof


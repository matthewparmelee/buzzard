# buzzard

## Problem
We want to know the most popular book title for each account in our
set of (fake) data.

## Input Data
We have a CSV of "usage session" data stored in a CSV called
``usage_sessions_20160930.csv``.  Each line represents a single session
of usage of a book for some company.  Each session has a
``start_time`` and an ``end_time``.  Each book is identified by a real ISBN.

## Steps
1. Fork this repository into your own account and write your code in
that forked copy of the repo.
2. Write some python to parse the CSV into rows of usage events.
3. Create table(s) in a SQLite database to store all of this data.
4. You can look up the titles corresponding to each ISBN using the
   Google Books API, e.g.
   ``https://www.googleapis.com/books/v1/volumes?maxResults=1&q=9781782161608``
   You'll want to make a request for each distinct ISBN in the data:
   ``q=<the_isbn>``
   (Try not to make a call to this API for each row in the data set)
5. Write a SQL query that will provide a list of the most popular
   book for each company.  Your program can simply print this list, or
   store the results in a table in your SQLite database, or anything
   else that seems reasonable.
6. Remember to commit and push your code to your repo when you're done
   so you can share it.

## Notes
Feel free to use any third party libraries you need,
(e.g. ``requests``). Remember that ``sqlite`` is part of the python
standard library: https://docs.python.org/3.6/library/sqlite3.html

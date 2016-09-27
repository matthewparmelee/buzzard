# generate

This module provides a small script, ``make_csv.py``, that generates a CSV
of fake usage data for a set of fake companies using real ISBNs:

    $ python generate/make_csv.py my-file.csv --number-companies 10 --number-isbns 5 --records-per-account 50

Required third-party libraries are located in ``requirements.txt``.

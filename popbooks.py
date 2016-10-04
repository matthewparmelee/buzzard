#!/usr/bin/env python

# Matt Parmelee
# October 03, 2016

# https://github.com/safarijv/buzzard

#####################################

# Imports
import requests
import pandas as pd
import sqlite3


def import_data(filename):
    """Import and clean usage data into database"""

    # Read data into dataframe
    df      = pd.read_csv(filename)
    indices = ",".join(df.columns.values)

    # Clean data
    fixed = []
    group = df.groupby('company').count(axis=1).sort('isbn', ascending=False)
    companies = group.index.values
    for company1 in companies:
        name1 = company1
        fixed.append(name1)
        for company2 in companies:
            name2 = company2

            if (name1 == name2) or (name2 in fixed):
                continue
            dist = levenshtein(name1, name2)
            if dist <= 3:
                df.replace(name2, name1, inplace=True)
                fixed.append(name2)

    # Instantiate db
    conn = sqlite3.connect("output.db")
    df.to_sql('usage', con=conn, if_exists='replace', chunksize=10000)
    conn.close()

def find_popular_books():
    """Query database to determine most popular book per company"""

    # Connect to db
    conn = sqlite3.connect("output.db")
    cur  = conn.cursor()

    # Query db
    sql = "SELECT company, isbn, MAX(time_spent) as time_spent FROM (SELECT company, isbn, SUM(julianday(datetime(end_time)) - julianday(datetime(start_time))) AS time_spent FROM usage GROUP BY isbn, company ORDER BY time_spent DESC) GROUP BY company;"
    
    # Store results
    df = pd.read_sql(sql, conn)
    df = df.drop('time_spent', 1)

    # Title lookups
    for isbn in df.isbn.unique():
        title = get_book_title(isbn)
        df.loc[df['isbn']==isbn, 'title'] = title

    # Commit to db
    df.to_sql('popular', con=conn, if_exists='replace', chunksize=10000)
    conn.close()

def output_book_list():
    """Output the popular books list for debugging purposes"""

    # Connect to db
    conn = sqlite3.connect("output.db")
    cur  = conn.cursor()
    cur.execute("SELECT * FROM popular")
    data = cur.fetchall()
    print "Company\tISBN\tTitle"
    print "-------------------------------------------"
    for index, company, isbn, title in data:
        print "{}\t{}\t{}".format(company, isbn, title.encode('utf-8'))
    conn.close()

def get_book_title(isbn):
    """Given an ISBN, determine a given book's title"""

    url   = "https://www.googleapis.com/books/v1/volumes?maxResults=1&key=AIzaSyCT_Gz7AygITqhtkG5YhYJSnAzXhEad1hE&q=" + str(isbn)
    r     = requests.get(url).json()

    if int(r["totalItems"]) > 0:
        title = r["items"][0]["volumeInfo"]["title"]
    else:
        title = "TITLE NOT FOUND"
    return title

def levenshtein(s1, s2):
    """Levenshtein distance implementation borrowed from Wikibooks in lieu of editdist package"""

    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

if __name__ == "__main__":
    # Parse data
    import_data("usage_sessions_20160930.csv")

    # Find most popular book for each company
    find_popular_books()

    # DEBUG: Output book list
    output_book_list()
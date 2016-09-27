import argparse
import csv
from datetime import datetime, timedelta
import json
import os
import random

from faker import Faker
import pytz

fake = Faker()


def get_companies(n=100):
    """
    :returns: A list of 100 fake company names.
    """
    companies = set()
    while len(companies) < n:
        companies.add(fake.company())

    return list(companies)


def perturb(string, likelihood=0.2):
    """
    :returns: With the given likelihood, returns a version of the provided string
    with two neighboring characters swapped.
    """
    if random.random() > likelihood:
        return string

    index = random.randint(1, len(string) - 2)
    characters = list(string)
    temp = characters[index]
    characters[index] = characters[index - 1]
    characters[index - 1] = temp
    return ''.join(characters)


def get_isbns():
    """
    :returns: A list of 100 real ISBNs.
    """
    directory = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(directory, 'isbn.json')) as f_in:
        return json.load(f_in)


def get_datetimes_between(start, end, n=100):
    """
    :returns: A list of 100 datetime objects (with UTC tzinfo) between
    the given start and end times.
    """
    return sorted([fake.date_time_between(start, end, tzinfo=pytz.utc)
                   for _ in range(n)])


def make_csv(filename,
             number_companies=25,
             number_isbns=25,
             records_per_account=1000):
    """
    For each of ``number_companies`` companies, generates usage records
    between two datetimes over a sample of ``number_isbns`` ISBNs.
    """
    assert number_companies <= 100
    assert number_isbns <= 100

    companies = get_companies()[:number_companies]
    isbns = get_isbns()[:number_isbns]

    header = ('company', 'isbn', 'start_time', 'end_time')
    with open(filename, 'w') as file_out:
        writer = csv.DictWriter(file_out, fieldnames=header)
        writer.writeheader()

        end = datetime.utcnow()
        start = end - timedelta(days=30)

        for company in companies:
            for start_time in get_datetimes_between(start,
                                                    end,
                                                    records_per_account):
                end_time = start_time + timedelta(minutes=random.randint(1, 30))
                isbn = random.choice(isbns)
                writer.writerow({
                    'company': perturb(company, 0.1),
                    'isbn': isbn,
                    'start_time': start_time,
                    'end_time': end_time
                })


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=(
        'Generates a CSV of fake usage sessions '
        'for fake companies (over real ISBNs)'))
    parser.add_argument('filename', help='The name of the CSV to generate')
    parser.add_argument('--number-companies',
                        help='The number of fake companies to generate usage data for')
    parser.add_argument('--number-isbns',
                        help='The number of ISBNs to use')
    parser.add_argument('--records-per-account',
                        help='The number of records to generate for each company')
    args = parser.parse_args()

    kwargs = {}
    for option in ('number_companies', 'number_isbns', 'records_per_account'):
        if getattr(args, option):
            kwargs[option] = int(getattr(args, option))

    print(kwargs)
    make_csv(args.filename, **kwargs)

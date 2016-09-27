import csv
import random

from faker import Faker
import pytz

fake = Faker()


def get_companies(n=100):
    companies = set()
    while len(companies) < n:
        companies.add(fake.company())

    return companies


def perturb(string, likelihood=0.2):
    if random.random() > likelihood:
        return string

    index = random.randint(1, len(string) - 2)
    characters = list(string)
    temp = characters[index]
    characters[index] = characters[index - 1]
    characters[index - 1] = temp
    return ''.join(characters)


def get_isbns():
    pass


def get_datetimes_between(start, end, n=100):
    return [fake.date_time_between(start, end, tzinfo=pytz.utc)
            for _ in range(n)]

from datetime import datetime

import pytz

from generate import make_csv


def test_get_companies():
    companies = make_csv.get_companies(10)
    assert 10 == len(companies)
    assert None not in companies


def test_perturb():
    assert 'act' == make_csv.perturb('cat', 1)
    assert 'cat' == make_csv.perturb('cat', 0)

    diff_count = 0
    original = 'declaration of independence'
    for _ in range(1000):
        perturbed = make_csv.perturb(original, .5)
        diff_count += int(perturbed == original)

    assert 400 <= diff_count <= 600


def test_get_isbns():
    assert 100 == len(make_csv.get_isbns())


def test_get_datetimes_between():
    start = datetime(2016, 1, 1, tzinfo=pytz.utc)
    end = datetime(2016, 1, 31, tzinfo=pytz.utc)
    datetimes = make_csv.get_datetimes_between(start, end)
    assert 100 == len(datetimes)

    for dt in datetimes:
        assert start <= dt <= end

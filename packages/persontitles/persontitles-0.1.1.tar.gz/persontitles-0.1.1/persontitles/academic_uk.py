#!/usr/bin/env python
# academic_uk.py
"""Collection of UK academic degrees."""
import unicodedata

import requests
from bs4 import BeautifulSoup


def degrees_uk() -> set:
    try:
        with open('./persontitles/academic_uk.txt', mode='r', encoding='utf-8') as fin:  # noqa
            ACADEMIC = fin.read().split('\n')
    except FileNotFoundError:
        DEGREES = _degrees()
        ACADEMIC = []
        for abbr in DEGREES:
            abbr = unicodedata.normalize('NFKD', abbr)
            ACADEMIC.append(abbr)
        with open('./persontitles/academic_uk.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in set(ACADEMIC)))
    return set(ACADEMIC)


def get_degrees(soup):
    degrees = []
    for li in soup.find_all('li'):
        values = [li.text]
        degrees.append(values[0])
    return degrees


def strip_degrees(degrees) -> list:
    abbrevs = []
    for i, degree in enumerate(degrees):
        abbr = degree.split('-')[0].strip()
        abbrevs.append(abbr.strip())
    return abbrevs


def final_degrees(abbrevs):
    final_degrees = []
    for abbr in abbrevs:
        if ' or ' in abbr:
            abbrs = abbr.split('or')
            for ab in abbrs:
                final_degrees.append(ab.strip())
        elif ',' in abbr:
            abbrs = abbr.split(',')
            for ab in abbrs:
                final_degrees.append(ab.strip())
        elif ') ' in abbr:
            abbrs = abbr.split(') ')
            ab = abbrs[0].strip()
            if ab[-1] != ')':
                ab = ab + ')'
            final_degrees.append(ab)
        else:
            final_degrees.append(abbr.strip())
    return final_degrees


def _degrees():
    data = requests.get('https://en.wikipedia.org/wiki/British_degree_abbreviations')  # noqa
    soup = BeautifulSoup(data.text, 'lxml')
    degrees = get_degrees(soup)
    uk_degrees = []
    for i, degree in enumerate(degrees):
        if i > 19 and i < 440:
            uk_degrees.append(degree)
    abbrevs = strip_degrees(uk_degrees)
    fnl_degrees = final_degrees(abbrevs)

    return fnl_degrees


if __name__ == '__main__':
    ACADEMIC_UK = degrees_uk()
    for i, degree in enumerate(ACADEMIC_UK):
        print(i, degree)

#!/usr/bin/env python
# academic_german.py
"""Collection of German academic degrees."""
import unicodedata

import requests
from bs4 import BeautifulSoup


# https://www.unker.com/de/akademische-titel
ADD = ['Dr. E. h.', 'Dr. eh.', 'Dr. jur.', 'Dr. iur. et rer. pol.']


def degrees_ger() -> set:
    try:
        with open('./persontitles/academic_german.txt', mode='r', encoding='utf-8') as fin:  # noqa
            ACADEMIC = fin.read().split('\n')
    except FileNotFoundError:
        degrees = _degrees()
        ACADEMIC = []
        for abbr in degrees:
            ACADEMIC.append(abbr)
        with open('./persontitles/academic_german.txt', mode='a', encoding='utf-8') as fout:  # noqa
            fout.write('\n'.join(item for item in set(ACADEMIC)))

    return set(ACADEMIC)


def get_degrees(soup):
    degrees = []
    for tr in soup.find_all('tr'):
        values = [td.text for td in tr.find_all('td')]
        try:
            degrees.append(values[0])
        except IndexError:
            # print("IndexError:", values)
            pass
    return degrees


def strip_degrees(degrees) -> list:
    abbrevs = []
    for degree in degrees:
        if '(' in degree:
            bracket_content = degree.split('(')[-1]
            if 'Master' in degree:
                degree = bracket_content.split(')')[0]
                abbrevs.append(degree)
            elif 'FH' in bracket_content:
                degree = degree.split(')')[0]
                degree = degree + ')'
                abbrevs.append(degree)
            elif 'Med.' in bracket_content:
                degree = degree.split(')')[0]
                degree = degree + ')'
                abbrevs.append(degree)
            elif 't.o.' in bracket_content:
                degree = degree.split(')')[0]
                degree = degree + ')'
                abbrevs.append(degree)
            else:
                degree = degree.split('(')[0]
                if '/' in degree:
                    for ttle in degree.split('/'):
                        abbrevs.append(ttle)
                else:
                    abbrevs.append(degree)
        elif len(set(degree)) == 1:
            pass
        elif 'oder' in degree:
            for ttle in degree.split('oder'):
                abbrevs.append(ttle.strip())
        elif '/' in degree:
            for ttle in degree.split('/'):
                if ttle == 'Kunstvermittlung':
                    abbrevs.append('Dipl. Kunstpädagogik/Kunstvermittlung')
                else:
                    abbrevs.append(ttle.strip())
        elif '[' in degree:
            abbrevs.append(degree.split('[')[0])
        else:
            abbrevs.append(degree)

    for degree in ADD:
        abbrevs.append(degree)

    return abbrevs


def final_degrees(abbrevs):
    final_degrees = []
    for abbr in abbrevs:
        # get rid of unicode's \xa0 for the empty spaces
        # https://stackoverflow.com/a/34669482/6597765
        abbr = unicodedata.normalize('NFKD', abbr)
        if len(set(abbr)) == 1:
            pass
        elif '[' in abbr:
            abbr = abbr.split('[')[0]
            final_degrees.append(abbr.strip())
        elif '...' in abbr:
            pass
        else:
            final_degrees.append(abbr.strip())
    return final_degrees


def _degrees():
    data = requests.get('https://de.wikipedia.org/wiki/Liste_akademischer_Grade_(Deutschland)')  # noqa
    soup = BeautifulSoup(data.text, 'lxml')
    degrees = get_degrees(soup)
    abbrevs = strip_degrees(degrees)
    degrees = final_degrees(abbrevs)

    return degrees


if __name__ == '__main__':
    ACADEMIC = degrees_ger()
    for i, degree in enumerate(ACADEMIC):
        print(i, degree)

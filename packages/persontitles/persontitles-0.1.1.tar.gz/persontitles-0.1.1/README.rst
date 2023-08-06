Overview
========

:deployment:

:test/coverage:
    .. image:: https://app.codacy.com/project/badge/Grade/4bb124e2a8334d608c6a4d1cf1d1e543
        :target: https://www.codacy.com/gh/0LL13/persontitles/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=0LL13/persontitles&amp;utm_campaign=Badge_Grade

    .. image:: https://codecov.io/gh/0LL13/persontitles/branch/main/graph/badge.svg?token=G7O54JQHFE
        :target: https://codecov.io/gh/0LL13/persontitles

:build status:

:docs:
    .. image:: https://img.shields.io/github/license/0LL13/persontitles
        :target: https://opensource.org/licenses/MIT


A dict with three lists containing academic degrees from the US, UK, and Germany.
A dict with peer titles from various countries.

Features
--------

Check if a degree is a valid degree of chosen country.
Check if a degree is written correctly.
Check the number of US, UK, and German academic degrees.
Check if a title is a valid peer title of chosen country.

Usage with degrees
------------------
::

    >>>from persontitles import academic_degrees
    >>>DEGREES = academic_degrees.degrees()

    >>>"Dr. iur. et rer. pol." in DEGREES["GER"]
    >>>True

    >>>"bogus degree" in DEGREES["GER"]
    >>>False

    >>>len(DEGREES["GER"])
    >>>418

    >>>"MOcean" in DEGREES["UK"]
    >>>True

    >>>"Dr. iur." in DEGREES["UK"]
    >>>False

    >>>len(DEGREES["UK"])
    >>>404

    >>>"B.App.Sc(IT)" in DEGREES["US"]
    >>>True

    >>>len(DEGREES["US"])
    >>>614

Usage with titles
-----------------
::

    >>>from persontitles import peertitles
    >>>TITLES = peertitles.peertitles()

    >>>"Pfalzgräfin" in TITLES["German"]
    >>>True

    >>>"Archduke" in TITLES["English"]
    >>>True


Credits
-------

Credits to all the unsung heroes who maintain and update the Wikipedia.

Installation
------------
::

    pip install persontitles

or

::

    pipenv install persontitles

Contribute
----------

| **The best way to contribute is to update a wiki page with degrees or titles.**
| If you update the wiki pages and rebuild a new collection, the added degrees will
| be included.

Support
-------


Planned
-------


Warranty
--------

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY
DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

License
-------

MIT License

Copyright (c) 2020 Oliver Stapel

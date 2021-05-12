AFL Tables Scraper
==================

The AFL Tables Scraper is a Python package and command-line executable that downloads Australian Football League (AFL)
match data from the fantastic database `AFL Tables <https://afltables.com/afl/afl_index.html>`_, and outputs it in
a structured, machine-readable form.

Full documentation available on `Github Pages <https://multimeric.github.io/AflTablesScraper>`_

Installation
------------
Note that this module requires python 3.5 and above

Install using:

.. code-block:: bash

    pip install afl_tables

Python Usage
------------

The AFL Tables module can be used to scrape matches as follows:

.. code-block:: python

    from afl_tables import MatchScraper

    # Make a scraper for a particular year (2015)
    rounds = MatchScraper.scrape(2015)


See the docs on `Round <https://tmiguelt.github.io/AflTablesScraper#afl_tables.Round>`_ for more information on how to use this object

CLI Usage
---------
The AFL Tables module also creates a command-line script called ``afltables``, which can be used to scrape data outside
of a python script. Usage is as follows

.. code-block:: none

    usage: Scrapes the AFL Tables website and returns JSON data representing the matches
       [-h] year

    positional arguments:
      year        The year to scrape

    optional arguments:
      -h, --help  show this help message and exit

Changelog
_________

0.0.2
~~~~~
* Fix for missing fields in the attendees/date/venue part of the table, for example in 2020
* Added some tests for the package

0.0.1
~~~~~
* Initial release

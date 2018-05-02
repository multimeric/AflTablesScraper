AFL Tables Scraper
==================

Full documentation available on `Github Pages <https://tmiguelt.github.io/AflTablesScraper>`_

Installation
------------
Note that this module requires python 3.5 and above

Install using:

.. code-block:: bash

    pip install git+https://github.com/TMiguelT/AflTablesScraper#egg=afl_tables

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


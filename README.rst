AFL Tables Scraper
==================

Installation
------------
Note that this module requires python 3.5 and above

Install using:

.. code-block:: bash

    pip install git+https://github.com/TMiguelT/AflTablesScraper#egg=afl_tables

Usage
-----

Currently the AFL Tables module can only scrape matches:

.. code-block:: python

    from afl_tables import MatchScraper

    # Make a scraper for a particular year (2015)
    rounds = MatchScraper.scrape(2015)


See the docs on `Round <https://tmiguelt.github.io/AflTablesScraper#afl_tables.Round>`_ for more information on how to use this object

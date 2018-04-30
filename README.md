# AFL Tables Scraper

## Installation
Note that this module requires python 3.5 and above

Install using:
```bash
pip install git+https://github.com/TMiguelT/AflTablesScraper#egg=afl_tables
```

## Usage
Currently the AFL Tables module can only scrape matches:
```
from afl_tables import MatchScraper

# Make a scraper for a particular year (2015)
scraper = MatchScraper(2015)

# Scrape the data into a list of matches
rounds = scraper.scrape()
```

For documentation on each class in the `rounds` array, refer to the source code or your IDE
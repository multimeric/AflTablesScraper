import argparse
import afl_tables
import json
import datetime
import sys


def get_args():
    parser = argparse.ArgumentParser('Scrapes the AFL Tables website and returns JSON data representing the matches')
    parser.add_argument('year', type=int, help='The year to scrape')
    return parser.parse_args()


def to_dict(obj):
    if isinstance(obj, datetime.datetime):
        return obj.replace(tzinfo=datetime.timezone.utc).timestamp()
    elif hasattr(obj, '__dict__'):
        return obj.__dict__


def main():
    args = get_args()
    matches = afl_tables.MatchScraper.scrape(args.year)
    json.dump(matches, sys.stdout, default=to_dict)


if __name__ == '__main__':
    main()

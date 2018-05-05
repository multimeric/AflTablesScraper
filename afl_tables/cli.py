import argparse
import afl_tables
import json
import datetime
import sys
from signal import signal, SIGPIPE, SIG_DFL

# Allow piping into tools like head
signal(SIGPIPE, SIG_DFL)


def get_args():
    parser = argparse.ArgumentParser('Scrapes the AFL Tables website and returns JSON data representing the matches')
    parser.add_argument('year', type=int, help='The year to scrape')
    return parser.parse_args()


def to_json(obj):
    if isinstance(obj, datetime.datetime):
        return obj.replace(tzinfo=datetime.timezone.utc).timestamp()
    elif isinstance(obj, afl_tables.TeamMatch):
        dict = obj.__dict__
        del dict['match']
        return dict
    elif hasattr(obj, '__dict__'):
        return obj.__dict__


def main():
    args = get_args()
    matches = afl_tables.MatchScraper.scrape(args.year)
    json.dump(matches, sys.stdout, default=to_json)


if __name__ == '__main__':
    main()

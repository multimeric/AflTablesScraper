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


def to_serializable_dict(obj):
    """
    Converts any AFL Tables object into a simple data structure of dicts and lists, which can be directly converted to
        json
    """
    if isinstance(obj, datetime.datetime):
        return obj.replace(tzinfo=datetime.timezone.utc).timestamp()
    elif isinstance(obj, (str, int, float)):
        return obj
    elif isinstance(obj, afl_tables.TeamMatch):
        d = obj.__dict__
        del d['match']
        return to_serializable_dict(d)
    elif isinstance(obj, dict):
        return {k: to_serializable_dict(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [to_serializable_dict(v) for v in obj]
    elif hasattr(obj, '__dict__'):
        return to_serializable_dict(obj.__dict__)


def main():
    args = get_args()
    matches = afl_tables.MatchScraper.scrape(args.year)
    json.dump(to_serializable_dict(matches), sys.stdout)


if __name__ == '__main__':
    main()

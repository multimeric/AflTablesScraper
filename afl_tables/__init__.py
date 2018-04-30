from urllib.parse import urljoin
import requests
import bs4
import itertools
import typing
from bs4 import BeautifulSoup

BASE_URL = 'https://afltables.com/afl/'


def grouper(n, iterable, fillvalue=None):
    """
    Chunks an iterable into chunks of size n
    """
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


class MatchException(Exception):
    pass


class Score:
    """
    Represents an AFL score for a single team at a given point in time
    """

    def __init__(self, goals, behinds):
        self.goals = goals
        self.behinds = behinds

    @classmethod
    def parse(cls, pointstring: str):
        """
        Parses a string in the form x.y
        """
        goals, behinds = pointstring.split('.')
        return Score(int(goals), int(behinds))

    @property
    def score(self):
        return 6 * self.goals + self.behinds

    def __str__(self):
        return f'{self.goals}.{self.behinds}'


class TeamRound:
    """
    Represents an individual team in an individual round
    """

    def __init__(self, name: str, scores: typing.Iterable[Score] = [], bye: bool = False):
        self.name = name
        self.scores = scores
        self.bye = bye

    @classmethod
    def parse_bye(cls, name: bs4.Tag):
        return cls(name=name.text, bye=True)

    @classmethod
    def parse_match(cls, name: bs4.Tag, rounds: bs4.Tag):
        return cls(name=name.text, scores=[Score.parse(s) for s in rounds.text.split()], bye=False)

    def __str__(self):
        if self.bye:
            return f'{self.name} Bye'
        else:
            return f'{self.name} {self.scores[-1]}'


class Match:
    """
    Represents a single match of AFL, with either two teams or one team (a bye)
    """

    @classmethod
    def parse(cls, table: bs4.Tag):
        """
        Parses a Match from the appropriate <table> element
        """
        td = table.find_all('td')

        if len(td) == 8:
            team_1, team_1_stats, team_1_score, misc, team_2, team_2_stats, team_2_score, winner = td
            return cls([TeamRound.parse_match(team_1, team_1_stats), TeamRound.parse_match(team_2, team_2_stats)])
        elif len(td) == 2:
            return cls([TeamRound.parse_bye(td[0])])
        else:
            raise MatchException('This is invalid markup for a Match object')

    def __init__(self, teams: typing.List[TeamRound]):
        self.teams = teams

    @property
    def bye(self):
        return self.teams[0].bye

    def __str__(self):
        if self.bye:
            return f'{self.teams[0].name} vs Bye'
        else:
            return f'{self.teams[0].name} vs {self.teams[1].name}'


class Round:
    """
    Represents a single round of AFL, with one or more matches being played in that round
    """

    @classmethod
    def parse(cls, title: bs4.Tag, table: bs4.Tag) -> 'Round':
        """
        Parses a round from two table elements that define it
        :param title: The <table> tag that contains this round's header
        :param table: The <table> tag that contains this round's data
        """
        title = title.text

        if 'Final' in title:
            matches = [Match.parse(table)]
        else:
            matches = []
            for match in table.select('td[width="85%"] table'):
                try:
                    matches.append(Match.parse(match))
                except MatchException:
                    continue

        return cls(title=title, matches=matches)

    def __init__(self, title: str, matches: list = []):
        self.title = title
        self.matches = matches

    def __str__(self):
        return self.title


class MatchScraper:
    def __init__(self, year: int):
        self.year = year

    @property
    def url(self):
        return urljoin(BASE_URL, f'seas/{self.year}.html')

    def scrape(self) -> typing.List[Round]:
        rounds = []
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html5lib')

        # Filter out irrelevant tables
        tables = [table for table in soup.select('center > table') if
                  table.get('class') != ['sortable'] and table.text != 'Finals']

        # Group the tables into title, content pairs
        for header, body in grouper(2, tables):
            title = header.find('td')

            rounds.append(Round.parse(title, body))

        return rounds

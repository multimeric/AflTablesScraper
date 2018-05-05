from urllib.parse import urljoin
import requests
import bs4
import datetime
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

    :ivar goals: Number of goals scored
    :ivar behinds: Number of behinds/points scored
    """

    goals: int
    behinds: int

    def __init__(self, goals, behinds):
        self.goals = goals
        self.behinds = behinds

    @classmethod
    def parse(cls, pointstring: str) -> 'Score':
        """
        Parses a string in the form x.y
        """
        goals, behinds = pointstring.replace('(', '').replace(')', '').split('.')
        return Score(int(goals), int(behinds))

    @property
    def score(self) -> int:
        """
        The calculated score as a single integer
        """
        return 6 * self.goals + self.behinds

    def __str__(self):
        return f'{self.goals}.{self.behinds}'


class TeamMatch:
    """
    Represents an individual team in an individual match

    :ivar name: The name of this team
    :ivar scores: A list of Score objects indicating the score of this team at the end of each of the four quarters.
        There may be 5 values in the array, in the case of extra time. In all cases, the final value in this array is
        the final score for this team
    :ivar match: The Match that this round belongs to
    """

    name: str
    scores: typing.List[Score]
    match: 'Match'

    def __init__(self, name: str, match: 'Match', scores: typing.List[Score] = []):
        self.name = name
        self.scores = scores
        self.match = match

    @property
    def final_score(self) -> typing.Optional[Score]:
        """
        Returns the final score of this team at the end of the match, or None, if this was a bye
        """
        if self.match.bye:
            return None
        else:
            return self.scores[-1]

    @classmethod
    def parse_bye(cls, name: bs4.Tag, match: 'Match'):
        return cls(name=name.text, match=match)

    @classmethod
    def parse_match(cls, name: bs4.Tag, rounds: bs4.Tag, match: 'Match'):
        return cls(name=name.text, scores=[Score.parse(s) for s in rounds.text.split()], match=match)

    def __str__(self):
        if self.match.bye:
            return f'{self.name} Bye'
        else:
            return f'{self.name} {self.final_score}'


class Match:
    """
    Represents a single match of AFL

    :ivar teams: A list of teams, with either two teams or one team (a bye)
    :ivar attendees: Number of attendees at this match
    :ivar date: The time and date that this match started
    :ivar venue: The name of the venue at which this match was played
    :ivar winner: The name of the winning team
    """

    teams: typing.List[TeamMatch]
    attendees: int
    date: datetime.datetime
    venue: str
    winner: str

    @classmethod
    def parse(cls, table: bs4.Tag):
        """
        Parses a Match from the appropriate <table> element
        """
        td = table.find_all('td')

        if len(td) == 8:
            team_1, team_1_stats, team_1_score, misc, team_2, team_2_stats, team_2_score, winner = td
            date, _, attendees, _, _, venue = misc
            simple_date = ' '.join(str(date).split(' ')[:4])
            parsed_date = datetime.datetime.strptime(simple_date, '%a %d-%b-%Y %I:%M %p')

            match = cls(
                [],
                date=parsed_date,
                venue=venue.text,
                attendees=int(str(attendees).replace(',', '').replace(' ', '')),
                bye=False,
                winner=winner.b.text
            )

            match.teams = [
                TeamMatch.parse_match(team_1, team_1_stats, match),
                TeamMatch.parse_match(team_2, team_2_stats, match)
            ]

            return match
        elif len(td) == 2:
            match = cls([], bye=True, winner=td[0].text)
            match.scores = [TeamMatch.parse_bye(td[0], match)]
            return match
        else:
            raise MatchException('This is invalid markup for a Match object')

    def __init__(self,
                 teams: typing.List[TeamMatch],
                 winner: str,
                 attendees: int = None,
                 date: datetime = None,
                 venue: str = None,
                 bye: bool = False):
        self.teams = teams
        self.attendees = attendees
        self.date = date
        self.venue = venue
        self.bye = bye
        self.winner = winner

    def __str__(self):
        if self.bye:
            return f'{self.teams[0].name} vs Bye'
        else:
            return f'{self.teams[0].name} vs {self.teams[1].name}'


class Round:
    """
    Represents a single round of AFL, with one or more matches being played in that round

    :ivar title: The human-readable title for this round
    :ivar matches: A list of matches played during this round
    """

    title: str
    matches: typing.List[Match]

    def __init__(self, title: str, matches: list = []):
        self.title = title
        self.matches = matches

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

    def __str__(self):
        return self.title


class MatchScraper:
    """
    A static class that can be used to scrape the matches from the AFL Tables website
    """

    @staticmethod
    def _url(year: int):
        """
        Returns the AFL Tables URL for the provided year
        """
        return urljoin(BASE_URL, f'seas/{year}.html')

    @classmethod
    def scrape(cls, year: int) -> typing.List[Round]:
        """
        Scrapes all the match data for the given year

        :param year: The year to scrape, e.g. 2015
        """
        url = cls._url(year)
        rounds = []
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'html5lib')

        # Filter out irrelevant tables
        tables = [table for table in soup.select('center > table') if
                  table.get('class') != ['sortable'] and table.text != 'Finals']

        # Group the tables into title, content pairs
        for header, body in grouper(2, tables):
            title = header.find('td')

            rounds.append(Round.parse(title, body))

        return rounds

from urllib.parse import urljoin
import requests
import bs4
import itertools
from bs4 import BeautifulSoup

BASE_URL = 'https://afltables.com/afl/'


def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.zip_longest(fillvalue=fillvalue, *args)


class Score:
    """
    Represents an AFL score for a single team at a given point in time
    """

    def __init__(self, goals, behinds):
        self.goals = goals
        self.behinds = behinds

    @classmethod
    def parse(cls, pointstring:str):
        """
        Parses a string in the form x.y
        """
        goals, behinds = pointstring.split('.')
        return Score(int(goals), int(behinds))

    @property
    def score(self):
        return 6 * self.goals + self.behinds


class TeamScores:
    def __init__(self, name: bs4.Tag, rounds: bs4.Tag):
        self.name = name.text
        self.scores = [Score.parse(s) for s in rounds.text.split()]


class Match:
    def __init__(self, table: bs4.Tag):
        team_1, team_1_stats, team_1_score, misc, team_2, team_2_stats, team_2_score, winner = table.find_all('td')
        self.teams = [TeamScores(team_1, team_1_stats), TeamScores(team_2, team_2_stats)]


class Round:
    def __init__(self, title: bs4.Tag, table: bs4.Tag):
        self.title = title.text
        self.matches = []
        for match in table.select('td[width="85%"] table'):
            self.matches.append(Match(match))


class MatchScraper:
    def __init__(self, year: int):
        self.year = year
        self.rounds = []

    @property
    def url(self):
        return urljoin(BASE_URL, f'seas/{self.year}.html')

    def scrape(self):
        html = requests.get(self.url).text
        soup = BeautifulSoup(html, 'html5lib')

        tables = soup.select('center > table')
        for header, body in grouper(2, tables):
            title = header.find('td')

            # Break if we're past the rounds
            if 'Round' not in title.text:
                break

            self.rounds.append(Round(title, body))

        return self.rounds


m = MatchScraper(2015)
m.scrape()
print(m)

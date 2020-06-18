from afl_tables import MatchScraper
import pytest
from datetime import datetime


@pytest.mark.parametrize('year', list(range(1908, 2021)))
def test_years(year):
    """
    Checks that each year doesn't crash, at least
    """
    MatchScraper.scrape(year)


def test_2019():
    """
    Check specific attributes of the result object for 2019
    """
    rounds = MatchScraper.scrape(2019)

    round_1 = rounds[0]
    assert round_1.title == 'Round 1'

    match_1 = round_1.matches[0]
    assert match_1.date == datetime(year=2019, month=3, day=21, hour=19, minute=25)
    assert match_1.venue == 'M.C.G.'
    assert match_1.winner == 'Richmond'

    assert match_1.teams[0].name == 'Carlton'
    assert match_1.teams[0].final_score.score == 64

    assert match_1.teams[1].name == 'Richmond'
    assert match_1.teams[1].final_score.score == 97


def test_2020():
    """
    Check specific attributes of the result object for 2020
    """
    rounds = MatchScraper.scrape(2020)

    round_1 = rounds[0]
    assert round_1.title == 'Round 1'

    match_1 = round_1.matches[0]
    assert match_1.date == datetime(year=2020, month=3, day=19, hour=19, minute=40)
    assert match_1.venue == 'M.C.G.'
    assert match_1.winner == 'Richmond'

    assert match_1.teams[0].name == 'Richmond'
    assert match_1.teams[0].final_score.score == 105

    assert match_1.teams[1].name == 'Carlton'
    assert match_1.teams[1].final_score.score == 81

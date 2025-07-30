from dataclasses import dataclass
from typing import List
from datetime import datetime
import deserialize
from Models.H2hEvent import H2hBookmaker, H2hEvent, H2hOutcome
import Clients.OddsApiClient as oddsApi

@dataclass
class Outcome:
    name: str
    price: float


@deserialize.parser("last_update", datetime.fromisoformat)
class Market:
    key: str
    last_update: datetime
    outcomes: List[Outcome]


@deserialize.parser("last_update", datetime.fromisoformat)
class Bookmaker:
    key: str
    title: str
    last_update: datetime
    markets: List[Market]


@deserialize.parser("commence_time", datetime.fromisoformat)
class Event:
    id: str
    sport_key: str
    sport_title: str
    commence_time: datetime
    home_team: str
    away_team: str
    bookmakers: List[Bookmaker]
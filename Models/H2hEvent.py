import datetime
from enum import Enum
from typing import List, Optional
from dataclasses import dataclass

class H2hOutcome(Enum):
        H = 'home_team'
        A = 'away_team'
        D = 'draw'

@dataclass
class H2hBet:
    id: str
    bookmaker: str
    home_team: str
    away_team: str
    commence_time: datetime
    odds: float
    sport_key: str
    guessed_outcome: H2hOutcome
    betAmount: float
    outcome: Optional[H2hOutcome]
    extra_notes: Optional[str]

@dataclass
class H2hBookmaker:
    title: str
    home_team_back_odds: float
    away_team_back_odds: float
    draw_back_odds: float

@dataclass
class H2hEvent:
    id: str
    sport_key: str
    commence_time: datetime
    home_team: str
    away_team: str
    bookmakers: List[H2hBookmaker]
    outcome: Optional[H2hOutcome] = None
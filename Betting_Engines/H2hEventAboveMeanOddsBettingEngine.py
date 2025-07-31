from dataclasses import dataclass
import sys
from Models.H2hEvent import H2hEvent, H2hBet, H2hOutcome
import pandas as pd

@dataclass
class H2hEventAboveMeanOddsBettingEngine:
    alpha: float 
    betOddsUpperLimit: float = sys.maxsize
    commision:float = 0.06
    betAmount: float = 100
    
    def __willBet(self, probabilityToAssess, probabilityAverage, alpha, commision=0, bet_odds_upper_limit=sys.maxsize):
        return ((1-commision) * probabilityToAssess + commision) > 1/max((probabilityAverage - alpha), 0.01) and probabilityToAssess < bet_odds_upper_limit
    
    def __getWorthyBets(self, bookmakers_df):
        worthyBets = []
        for index, bookmaker in bookmakers_df.iterrows():
            for outcome in ["home_team", "away_team", "draw"]:
                if(bookmaker[f"{outcome}_back_odds"] is None):
                    break
                probabilityMedian = 1/bookmakers_df[f"{outcome}_back_odds"].median(numeric_only=True)
                if(self.__willBet(bookmaker[f"{outcome}_back_odds"], probabilityMedian, self.alpha, self.commision, self.betOddsUpperLimit)):
                    worthyBets.append({"bookmaker": bookmaker["title"], "guessed_outcome": H2hOutcome(outcome), "odds": bookmaker[f"{outcome}_back_odds"], "median": 1/probabilityMedian})
        return worthyBets

    def analyseAndFindBets(self, h2hEvents: list[H2hEvent]) -> list[H2hBet]: 
        events_df = pd.DataFrame(h2hEvents).sort_values(by='commence_time', ascending=True)
        for index, event in events_df.iterrows():
            bookmakers_df = pd.DataFrame(event["bookmakers"])
            if(len(bookmakers_df) == 0):
                continue

            print(self.__getWorthyBets(bookmakers_df))
            worthyBetsFound = self.__getWorthyBets(bookmakers_df)
            if(len(worthyBetsFound) == 0):
                print("no bets found")
                return

            betsFound = []
            for betFound in worthyBetsFound:
                betsFound.append(
                    H2hBet(
                        id= event.id,
                        sport_key=event.sport_key,
                        home_team=event.home_team,
                        away_team=event.away_team,
                        commence_time=event.commence_time,
                        bookmaker=betFound["bookmaker"],
                        betAmount=self.betAmount,
                        guessed_outcome=betFound["guessed_outcome"],
                        odds=betFound["odds"],
                        outcome=event.outcome,
                        extra_notes=f"median = {betFound["median"]}"
                    )
                )
            return betsFound
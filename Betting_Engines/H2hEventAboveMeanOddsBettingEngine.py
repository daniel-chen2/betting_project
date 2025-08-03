from dataclasses import dataclass
import sys
from Models.H2hEvent import H2hEvent, H2hBet, H2hOutcome
import pandas as pd

@dataclass
class H2hEventAboveMeanOddsBettingEngine:
    alpha: float 
    betOddsUpperLimit: float = sys.maxsize
    commision:float = 0.00
    betAmount: float = 100
    singleBookmaker: str = None
    
    def __willBet(self, probabilityToAssess, probabilityAverage, alpha, commision=0, bet_odds_upper_limit=sys.maxsize):
        return ((1-commision) * probabilityToAssess + commision) > 1/max((probabilityAverage - alpha), 0.01) and 1/probabilityAverage < bet_odds_upper_limit
    
    def __getWorthyBets(self, bookmakers_df):
        worthyBets = []
        # for index, bookmaker in bookmakers_df.iterrows():
        for outcome in ["home_team", "away_team", "draw"]:
            # Janky - Comment out highest bookmaker
            # highest_bookmaker_index = bookmakers_df[f"{outcome}_back_odds"].idxmax() 
            # if(pd.isna(highest_bookmaker_index)):
            #     continue
            # bookmaker = bookmakers_df.loc[bookmakers_df[f"{outcome}_back_odds"].idxmax()] 

            bookmaker_query = bookmakers_df.query(f"title.str.contains('{self.singleBookmaker}')", engine="python")
            if(len(bookmaker_query) == 0 ):
                continue
            bookmaker = bookmaker_query.iloc[0]

            if(bookmaker[f"{outcome}_back_odds"] is None or pd.isna(bookmaker[f"{outcome}_back_odds"])):
                continue
            probabilityMedian = 1/bookmakers_df[f"{outcome}_back_odds"].median(numeric_only=True)
            if(self.__willBet(bookmaker[f"{outcome}_back_odds"], probabilityMedian, self.alpha, self.commision, self.betOddsUpperLimit)):
                worthyBets.append({"bookmaker": bookmaker["title"], "guessed_outcome": H2hOutcome(outcome), "odds": bookmaker[f"{outcome}_back_odds"], "median": 1/probabilityMedian, "number_of_bookmakers": len(bookmakers_df)})
                # Remove later just to test
                break
                    
        return worthyBets

    def analyseAndFindBets(self, h2hEvents: list[H2hEvent]) -> list[H2hBet]: 
        events_df = pd.DataFrame(h2hEvents).sort_values(by='commence_time', ascending=True)
        betsFound = []
        for index, event in events_df.iterrows():
            bookmakers_df = pd.DataFrame(event["bookmakers"]) 
            if(len(bookmakers_df) == 0):
                continue
            worthyBetsFound = self.__getWorthyBets(bookmakers_df)
            if(len(worthyBetsFound) == 0):
                continue

            for betFound in worthyBetsFound:
                b = (betFound["odds"] - 1)
                p = (1/betFound["median"])
                kellyBetRatio = ((b * p) - (1-p))/b 
                betsFound.append(
                    H2hBet(
                        id= event.id,
                        sport_key=event.sport_key,
                        home_team=event.home_team,
                        away_team=event.away_team,
                        commence_time=event.commence_time,
                        bookmaker=betFound["bookmaker"],
                        betAmount=self.betAmount,
                        kellyBetRatio=kellyBetRatio,
                        halfKellyBetRatio=kellyBetRatio/2,
                        bookmaker_average_odds=betFound["median"],
                        guessed_outcome=betFound["guessed_outcome"],
                        odds=betFound["odds"],
                        number_of_bookmakers=betFound["number_of_bookmakers"],
                        outcome=event.outcome,
                        alpha=1/betFound["median"] - 1/betFound["odds"]
                    )
                )
        return betsFound
import pandas as pd
import numpy as np
import Clients.OddsApiClient as oddsApi
import sys
from Models.H2hEvent import H2hEvent, H2hBookmaker
from Transformers.H2hEventTransformer import oddsApiEventsToH2hEvent
import importlib
from datetime import datetime, timedelta, timezone
import Betting_Engines.H2hEventAboveMeanOddsBettingEngine as BettingEngine
import sys
import discord_bot as discord_bot

current_utc_time = datetime.now(timezone.utc)
future_time = current_utc_time + timedelta(hours=12)
iso_formatted_time_with_z = future_time.isoformat(timespec="seconds").replace(
    "+00:00", "Z"
)
current_formatted_time = current_utc_time.isoformat(timespec="seconds").replace(
    "+00:00", "Z"
)

sports = oddsApi.ALL_SOCCER_SPORTS + oddsApi.All_OTHER_SPORTS
soccer_events = oddsApi.getEventsForMultipleSports(
    sports=sports[4:10],
    regions=[oddsApi.Regions.UK],
    markets=[oddsApi.Markets.H2H],
    commenceTimeTo=iso_formatted_time_with_z,
    commenceTimeFrom=current_formatted_time,
)

bettingEngine = BettingEngine.H2hEventAboveMeanOddsBettingEngine(
    alpha=0,
    betOddsUpperLimit=2.5,
    betAmount=10,
    commision=0.0,
    singleBookmaker="betfair",
)

current_utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

result_df = pd.DataFrame(
    bettingEngine.analyseAndFindBets(oddsApiEventsToH2hEvent(soccer_events))
)
csv = result_df.to_csv(f"Results/{current_utc_time}_results.csv", index=False)

print(result_df)

if len(result_df) > 0:
    print("Sending message to discord...")
    for index, result in result_df.iterrows():
        discord_bot.send_message(
            f"\n\n bookmaker: {result["bookmaker"]} \n home_team: {result["home_team"]} \n away_team: {result['away_team']} \n commence_time: {result["commence_time"]} \n odds: {result["odds"]} \n bet amount: {result["betAmount"]} \n bookmaker average odds {result["bookmaker_average_odds"]}"
        )

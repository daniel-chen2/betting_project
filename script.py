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
import sys

sys.stdout.reconfigure(encoding='utf-8')

current_utc_time = datetime.now(timezone.utc)
future_time = current_utc_time + timedelta(hours=5)
iso_formatted_time_with_z = future_time.isoformat(timespec="seconds").replace(
    "+00:00", "Z"
)
current_formatted_time = current_utc_time.isoformat(timespec="seconds").replace(
    "+00:00", "Z"
)

sports = oddsApi.ALL_SOCCER_SPORTS + oddsApi.All_OTHER_SPORTS
soccer_events = oddsApi.getEventsForMultipleSports(
    sports=sports,
    regions=[oddsApi.Regions.UK],
    markets=[oddsApi.Markets.H2H],
    commenceTimeTo=iso_formatted_time_with_z,
    commenceTimeFrom=current_formatted_time,
)

bettingEngine = BettingEngine.H2hEventAboveMeanOddsBettingEngine(
    alpha=0.035,
    betOddsUpperLimit=2.25,
    betAmount=10,
    commision=0.06,
    singleBookmaker="betfair_ex_uk",
)

current_utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

result_df = pd.DataFrame(bettingEngine.analyseAndFindBets(oddsApiEventsToH2hEvent(soccer_events)))
csv_url = f'Results/{current_utc_time}_results.csv'
result_df.to_csv(csv_url, index=False) 

if(len(result_df) > 0):
    discord_bot.send_message("Results:", csv_url)

print(result_df)

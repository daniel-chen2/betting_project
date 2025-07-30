import requests
from enum import Enum
import deserialize
import Clients.OddsApiModel as oddsModel

API_KEY = '157d6795bd369c260d82ddb6064eb13f'

ODDS_API_URL = 'https://api.the-odds-api.com/v4'

class Regions(Enum):
    UK = 'uk'

class Markets(Enum):
    H2H = 'h2h'

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

ALL_SOCCER_SPORTS = [
    "soccer_argentina_primera_division",
    "soccer_austria_bundesliga",
    "soccer_belgium_first_div",
    "soccer_brazil_campeonato",
    "soccer_brazil_serie_b",
    "soccer_chile_campeonato",
    "soccer_china_superleague",
    "soccer_concacaf_leagues_cup",
    "soccer_conmebol_copa_libertadores",
    "soccer_conmebol_copa_sudamericana",
    "soccer_denmark_superliga",
    "soccer_efl_champ",
    "soccer_england_efl_cup",
    "soccer_england_league1",
    "soccer_england_league2",
    "soccer_epl",
    "soccer_fifa_world_cup_qualifiers_europe",
    "soccer_fifa_world_cup_winner",
    "soccer_finland_veikkausliiga",
    "soccer_france_ligue_one",
    "soccer_france_ligue_two",
    "soccer_germany_bundesliga",
    "soccer_germany_bundesliga2",
    "soccer_germany_liga3",
    "soccer_greece_super_league",
    "soccer_italy_serie_a",
    "soccer_japan_j_league",
    "soccer_korea_kleague1",
    "soccer_league_of_ireland",
    "soccer_mexico_ligamx",
    "soccer_netherlands_eredivisie",
    "soccer_norway_eliteserien",
    "soccer_poland_ekstraklasa",
    "soccer_spain_la_liga",
    "soccer_spain_segunda_division",
    "soccer_spl",
    "soccer_sweden_allsvenskan",
    "soccer_sweden_superettan",
    "soccer_switzerland_superleague",
    "soccer_turkey_super_league",
    "soccer_uefa_champs_league_qualification",
    "soccer_usa_mls",
]

def __getAllSports():
    sports_response = requests.get(
        f'{ODDS_API_URL}/sports', 
        params={
            'api_key': API_KEY
        }
    )

    if sports_response.status_code != 200:
        print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

    return sports_response.json()

def getEventsForMultipleSports(sports: list[str], regions: list[Regions], markets: list[Markets]) -> list[oddsModel.Event]:
    events_in_json = []
    for sport in sports:
        events_in_json.extend(__getEventsForSingleSport(sport, ",".join([region.value for region in list(regions)]), ",".join([market.value for market in list(markets)])))

    deserialised_events = []
    for event in events_in_json:
        deserialised_events.append(deserialize.deserialize(oddsModel.Event, event))
    
    return deserialised_events

def __getEventsForSingleSport(sport, regions, markets):
    odds_json = []

    odds_response = requests.get(

        f"https://api.the-odds-api.com/v4/sports/{sport}/odds",
        params={
            "api_key": API_KEY,
            "regions": regions,
            "markets": markets,
            "oddsFormat": ODDS_FORMAT,
            "dateFormat": DATE_FORMAT,
        },
    )


    if odds_response.status_code != 200:

        print(
            f"Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}"
        )


    else:

        odds_json = odds_response.json()

        print("Number of events:", len(odds_json))

        print(odds_json)


        # Check the usage quota

        print("Remaining requests", odds_response.headers["x-requests-remaining"])

        print("Used requests", odds_response.headers["x-requests-used"])

    return odds_json
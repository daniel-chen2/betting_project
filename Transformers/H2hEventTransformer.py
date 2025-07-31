from Clients import OddsApiClient
from Clients.OddsApiModel import Event
from Models.H2hEvent import H2hBookmaker, H2hEvent

def oddsApiEventsToH2hEvent(oddsApiEvents: list[Event]) -> list[H2hEvent]:
    # print(oddsApiEvents)
    return [oddsApiEventToH2hEvent(oddsApiEvent) for oddsApiEvent in oddsApiEvents]

def oddsApiEventToH2hEvent(oddsApiEvent: Event) -> H2hEvent:
    bookmakers = oddsApiEvent.bookmakers
    h2hBookmakers = []

    for bookmaker in bookmakers:
        allMarkets = bookmaker.markets

        h2hMarket = next(filter(lambda market: market.key == OddsApiClient.Markets.H2H.value, allMarkets), None)
        if(h2hMarket == None):
            continue

        h2hOutcomes = h2hMarket.outcomes

        draw_odds = next(filter(lambda outcome: outcome.name == "Draw", h2hOutcomes), None)

        h2hBookmakers.append(H2hBookmaker(
            title=bookmaker.key,
            home_team_back_odds=next(filter(lambda outcome: outcome.name == oddsApiEvent.home_team, h2hOutcomes)).price,
            away_team_back_odds=next(filter(lambda outcome: outcome.name == oddsApiEvent.away_team, h2hOutcomes)).price,
            draw_back_odds= draw_odds.price if draw_odds is not None else draw_odds
        ))
        
    return H2hEvent(
        id=oddsApiEvent.id,
        commence_time=oddsApiEvent.commence_time,
        sport_key=oddsApiEvent.sport_key,
        home_team=oddsApiEvent.home_team,
        away_team=oddsApiEvent.away_team,
        bookmakers=h2hBookmakers,
        outcome=None
    )
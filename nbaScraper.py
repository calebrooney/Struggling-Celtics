# https://www.nba.com/stats/teams/boxscores-traditional?OpponentTeamID=1610612738&Season=2016-17&SeasonType=Regular+Season
#scrape nba advance box scores
#https://www.nba.com/stats/teams/boxscores-traditional



import requests
from bs4 import BeautifulSoup
import pandas as pd



teams = ['ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
TeamIDs = {'ATL':1610612737, 'BOS':1610612738,'BRK':1610612751, 'CHI':1610612741, 'CHO':1610612766, 'CLE':1610612739, 'DAL':1610612742, 'DEN':1610612743, 'DET':1610612765, 'GSW':1610612744, 'HOU':1610612745, 'IND':1610612754, 'LAC':1610612746, 'LAL':1610612747, 'MEM':1610612763, 'MIA':1610612748, 'MIL':1610612749, 'MIN':1610612750, 'NOP':1610612740, 'NYK':1610612752, 'OKC':1610612760, 'ORL':1610612753, 'PHI':1610612755, 'PHO':1610612756, 'POR':1610612757, 'SAC':1610612758, 'SAS':1610612759, 'TOR':1610612761, 'UTA':1610612762, 'WAS':1610612764}
seasonTypes = ["Regular+Season", "Playoffs","PlayIn","Pre+Season","IST"]


def importBoxScores(team, season, seasonType = "Regular+Season"):
    
    if type(season) != str or len(season) != 7:
        print("Invalid season format. Please use the format 'YYYY-YY'")
        return

    OppTeamID = TeamIDs[team]
    url = f"https://www.nba.com/stats/teams/boxscores-traditional?OpponentTeamID={str(OppTeamID)}&Season={season}&SeasonType={seasonType}"
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.find_all("table")
    df = pd.read_html(str(tables))
    print(url)
    print(df)

#importBoxScores('BOS', '2022-23')
#current output : bullshit calendar

# get NBA.com player ID for given player
# playerIDS found thanks to Wfordh on github https://github.com/wfordh/ottobasket_values/blob/main/data/mappings_update_2023-09-14.csv

def getPlayerID(player_name):

    df = pd.read_csv("Player_IDs_update_2023-09-14.csv")
    NBA_ID_List =df['nba_player_id'].tolist()
    NBA_ID_List = [str(x)[:-2] for x in NBA_ID_List]
    nba_IDs = {k:v for k,v in zip(df['name'], NBA_ID_List)} # zip function to create dictionary of player names and IDs

    player_name = player_name.title()
    if player_name not in nba_IDs.keys():
        print("Player not found. Please check the spelling of the player's name.")
        return
    return nba_IDs[player_name]

# print(getPlayerID("Victor Wembanyama"))
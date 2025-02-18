import pandas as pd
import matplotlib.pyplot as plt
import os
import time
from bRefScraper import player_advBoxScore, getPlayerID
from datagrabber import importADVbyTeam

teams = ['ATL', 'BOS', 'BRK', 'CHI', 'CHO', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM', 'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHO', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']

# get celtics team data for Mazzulla era ('22-'23 to '24-'25)

# only call importADVbyTeam once, dont call if the JSON file already exists
if "ADVPlayerData_BOS.json" not in os.listdir():
    celts = importADVbyTeam("BOS")

celts = pd.read_json("ADVPlayerData_BOS.json")

celts = celts[celts['season'] >= 2023]

#new JSON with season range

celts.to_json("ADVPlayerData_BOS_2023-2025.json", orient='records')


print(celts["playerName"].unique())

# #probabale rate limit issue, likely not worth the effort
# #get advanced box scores 
# for year in celts["season"].unique():
#     for player in celts[celts["season"] == year]["playerName"].unique():
#         print(f"Processing data for {player} in season {year}")
#         time.sleep(5) #rate limit issue?
#         player_advBoxScore(player, year, saveJSON=True)

player_advBoxScore("Jayson Tatum", 2023, saveJSON=True)

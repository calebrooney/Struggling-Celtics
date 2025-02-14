import requests
from bs4 import BeautifulSoup
import pandas as pd
# from datagrabber import getPlayerID #you can do this i guess

# AD basktball reference 21-22  regular season
playerStats_url = "https://www.basketball-reference.com/players/d/davisan02/gamelog-advanced/2022/"
playerRequest = requests.get(playerStats_url)

playerSoup = BeautifulSoup(playerRequest.content, 'lxml')

player_per_game = playerSoup.find(name = 'table', attrs = {'id' : 'pgl_advanced'})

df_list = pd.read_html(str(player_per_game)) #creates list of len 1 dataframes
df = df_list[0]

def getPlayerID(player_name):

    df = pd.read_csv("Player_IDs_update_2023-09-14.csv")
    bref_id_List = df['bref_id'].tolist()

    bref_IDs = {k:v for k,v in zip(df['name'], bref_id_List)} # zip function to create dictionary of player names and IDs

    player_name = player_name.title() #allows for case insensitivity (except for names like 'DeMar DeRozan' or 'LeBron James')
    name_list = list(bref_IDs.keys())

    if player_name not in name_list:
        print("Player not found. Please check the spelling of the player's name and capitalize all appropriate lettters.")
        return
    return bref_IDs[player_name]

def player_advBoxScore(player: str, season: int):

    # if type(season) == int:
    #     return "Season must be a year (int) between 2000 and 2023"

    try:
        playerID = getPlayerID(player)
 
        if getPlayerID == None:
            print("Player not found, try again.")
            return

        playerStats_url = f"https://www.basketball-reference.com/players/d/{playerID}/gamelog-advanced/{season}/"
        playerRequest = requests.get(playerStats_url)
        playerSoup = BeautifulSoup(playerRequest.content, 'lxml')

        player_per_game = playerSoup.find(name = 'table', attrs = {'id' : 'pgl_advanced'})

        df_list = pd.read_html(str(player_per_game)) #creates list of len 1 dataframes
        df = df_list[0]

        ## cleaning df
        #get rid of extra column name rows
        df = df[df["Rk"] != "Rk"]
        df.reset_index(drop=True, inplace=True)

        return df

    except ImportError: ## 'html5lib not found' if player not in IDs csv
        return 
    

print(player_advBoxScore("Luke Kennard", 2022))
print(player_advBoxScore("jayson tatum", 2022))




##thanks to Gabriel Cano 
# https://medium.com/analytics-vidhya/web-scraping-nba-data-with-pandas-beautifulsoup-and-regex-pt-1-e3d73679950a

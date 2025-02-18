import requests
from bs4 import BeautifulSoup
import pandas as pd

## example link: AD basktball reference 21-22 regular season
## "https://www.basketball-reference.com/players/d/davisan02/gamelog-advanced/2022/"

def getPlayerID(player_name): #returns basketball reference ID for given player

    df = pd.read_csv("Player_IDs_update_2023-09-14.csv")
    bref_id_List = df['bref_id'].tolist()
    bref_IDs = {k:v for k,v in zip(df['name'], bref_id_List)} # zip function to create dictionary of player names and IDs

    player_name = player_name.title() #allows for case insensitivity (except for names like 'DeMar DeRozan' or 'LeBron James')
    name_list = list(bref_IDs.keys())

    if player_name not in name_list:
        print(f"{player_name} not found. Please check the spelling of the player's name and capitalize all appropriate lettters.")
        return
    return bref_IDs[player_name]

def player_advBoxScore(player: str, season: int, saveJSON=False): #returns DF of advanced box scores for player in given season
    try:
        playerID = getPlayerID(player)
        if playerID is None:
            print("Player not found, try again.")
            return None

        playerStats_url = f"https://www.basketball-reference.com/players/d/{playerID}/gamelog-advanced/{season}/"
        playerRequest = requests.get(playerStats_url)
        playerSoup = BeautifulSoup(playerRequest.content, 'lxml')

        player_per_game = playerSoup.find(name='table', attrs={'id': 'pgl_advanced'})

        df_list = pd.read_html(str(player_per_game)) #creates list of len 1 dataframes
        df = df_list[0]

        ## cleaning df
        #get rid of extra column name rows
        df = df[df["Rk"] != "Rk"].copy()  # copy() to avoid SettingWithCopyWarning
        df.reset_index(drop=True, inplace=True)

        #unnamed_5 --> home/away col
        df.loc[:, "Unnamed: 5"] = df["Unnamed: 5"].fillna("Home")
        df.loc[:, "Unnamed: 5"] = df["Unnamed: 5"].replace({"@": "Away"})
        df.rename(columns={"Unnamed: 5": "Home/Away"}, inplace=True)

        #rename and split unnamed_7 col
        df.rename(columns={"Unnamed: 7": "Result"}, inplace=True)
        result_margin_split = df["Result"].str.split("(", expand=True)
        df.loc[:, "Result"] = result_margin_split[0].str.strip()
        df.loc[:, "Margin"] = result_margin_split[1].str.replace(")", "", regex=True).str.replace("+", "", regex=True).str.strip()

        # Move the Margin column to the desired position
        col = df.pop('Margin')
        df.insert(df.columns.get_loc("Result") + 1, col.name, col)
        
        #remove age column
        df.drop(columns = ["Age"], inplace= True)

        #set columns to appropriate data types
        float_columns = df.columns[-17:]
        df[float_columns] = df[float_columns].apply(pd.to_numeric, errors='coerce').astype('float64')

        df[df.columns[0]] = df[df.columns[0]].apply(pd.to_numeric, errors='coerce').astype('int64')

        str_columns = df.columns[3:7]
        df[str_columns] = df[str_columns].astype('str')

        df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d')


        if saveJSON:
            df.to_json(f"{player}_{season}_advBoxScore.json", orient='records',indent=2)

        return df

    except ImportError: ## 'html5lib not found' if player not in IDs csv
        print("html5lib not found. Please install it.")
        return None


## view all columns
# pd.set_option('display.max_columns', None)
# pd.set_option('display.expand_frame_repr', False)

## Example usage
# AC22 = player_advBoxScore("Alex Caruso", 2022, saveJSON=True)

# print(AC22.head())
# print(AC22.tail())
# print(AC22.dtypes) 

# thanks to Gabriel Cano 
# https://medium.com/analytics-vidhya/web-scraping-nba-data-with-pandas-beautifulsoup-and-regex-pt-1-e3d73679950a

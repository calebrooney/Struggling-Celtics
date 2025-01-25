import pandas as pd
import matplotlib.pyplot as plt



celts_all_seasons = pd.read_json("BOSallseasonsteamdata.json") 

#print(celts_all_seasons)
#print()

#create list of celts_all_seasons columns 
#columns = list(celts_all_seasons)
#print(columns)

#series of season

seasons = celts_all_seasons['season']

print(seasons)
#from URL

import pandas as pd

df = pd.read_json("http://rest.nbaapi.com/api/PlayerDataTotals/team/BOS") 

#from JSON

import pandas as pd

celts_all_seasons = pd.read_json("BOSallseasonsteamdata.json") 

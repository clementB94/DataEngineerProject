from pymongo import MongoClient
import pandas as pd

client = MongoClient(host="mongodb", port=27017)

def insert_db():

    db = client['football_db']
    years = [1213, 1314, 1415, 1516, 1617, 1718, 1819]

    for league in ['ligue1', 'premiereleague', 'seria', 'bundesliga', 'laliga']:
        db[league].drop()
        li = []
        for year in years:
            df = pd.read_csv(f"/app/data_to_insert/{league}/season-{year}_csv.csv", index_col=None, header=0)
            li.append(df)
        df_to_insert = pd.concat(li, axis=0, ignore_index=True)

        db[league].insert_many(df_to_insert.to_dict('records'))

    for league in ['championsleague', 'europaleague']:
        db[league].drop()
        df_to_insert = pd.read_csv(f"/app/data_to_insert/{league}.csv", index_col=None, header=0)

        db[league].insert_many(df_to_insert.to_dict('records'))
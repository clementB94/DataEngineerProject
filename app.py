from flask import Flask, make_response, render_template, request, redirect
from pymongo import MongoClient

import pandas as pd
import plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

from real_time_scraping import rt_scrap
from insert_db import insert_db

app = Flask(__name__)   

client = MongoClient(host="mongodb", port=27017)

available_league = ['ligue1', 'premiereleague', 'seria', 'laliga', 'bundesliga', 'championsleague', 'europaleague']

def get_db():
    db = client['football_db']
    return db
    

### Defining routes and callbacks

@app.route('/')
def redirect_to_base():
    # redirect to the main page
    return redirect("http://localhost:5000/football", code=302)

@app.route('/callback', methods=['POST', 'GET'])
def cb():
    # callback so that the league graphs are updated
    return get_strongest_club(request.args.get('data'), int(request.args.get('range')))

@app.route('/callbacksearch', methods=['POST', 'GET'])
def search():
    # callback to update players statistics
    a, b, c, d, e, f, g, h, i = rt_scrap(request.args.get('data'))
    return {"a": a, "b": b, "c": c, "d": d, "e": e, "f": f, "g": g, "h": h, "i": i}

@app.route('/football')
def render():
    # render the main html file with a graph
    return render_template("football.html", graphJSON=get_strongest_club())

@app.route('/getPlotCSV/<ligue>', methods=['POST', 'GET'])
def dl(ligue):
    # Download a csv file from a mongodb collection
    if ligue in available_league: 
        db = client['football_db']
        cursor = db[ligue].find()
        df =  pd.DataFrame(list(cursor)).iloc[: , 1:] # remove 1st column which is mongodb's _id
        csv = df.to_csv(index=False)
        response = make_response(csv)
        cd = 'attachment; filename='+ligue+'.csv'
        response.headers['Content-Disposition'] = cd 
        response.mimetype='text/csv'

        return response

    else:
        return redirect("http://localhost:5000/football", code=302)

@app.route('/getPlotCSV/')
def redirection():
    # redirect to the main page
    return redirect("http://localhost:5000/football", code=302)


### Function that take a league and return a figure with plotly graphs (Bar, Scatter and Table)

def get_strongest_club(ligue='ligue1', size=20):

    db = get_db()

    if ligue == 'championsleague' or ligue == 'europaleague':

        # get data that we want from MongoDB database
        strongest_clubs = db[ligue].aggregate([{"$group" : {"_id" : "$Team",
        "average_goals_by_comps" : {"$avg" : "$Goal"},
        "average_taken_goals_by_comps" : {"$avg" : "$Goal_against"},
        "total_goals" : {"$sum" : "$Goal"},
        "total_taken_goals" : {"$sum" : "$Goal_against"},
        "matched_played" : {"$sum" : "$Match_played"},
        "average_points" : {"$avg" : "$Pts"},
        "average_matches_by_comps" : {"$avg" : "$Match_played"} }}])

        # create dataframe and new columns
        df = []
        for x in strongest_clubs:
            df.append([x['_id'], x['average_goals_by_comps'], x['average_taken_goals_by_comps'], x['average_matches_by_comps'], 
            x['matched_played'], x['average_points'], x['total_goals'], x['total_taken_goals']])
        df = pd.DataFrame(df, columns = ['Club', 'average_goals_by_comps', 'average_taken_goals_by_comps', 'average_matches_by_comps', 
        'matched_played', 'average_points', 'total_goals', 'total_taken_goals'])

        df['average_goals'] = df['average_goals_by_comps']/df['average_matches_by_comps']
        df['average_taken_goals'] = df['average_taken_goals_by_comps']/df['average_matches_by_comps']
        df['diff'] = df['average_goals'] - df['average_taken_goals']
        df['total_diff'] = df['total_goals'] - df['total_taken_goals']
        df = df.sort_values(by=['diff'], ascending=False)
        df['average_points'] = df['average_points'].round(2)

        # create figure
        fig = make_subplots(rows=2, cols=1, vertical_spacing=0.1, specs=[[{"type": "bar"}], [{"type": "table"}]])
        fig.add_trace(go.Bar(name='Average Goals By Club', x=df['Club'][0:size], y=df['average_goals'][0:size]), row=1, col=1)
        fig.add_trace(go.Bar(name='Average Taken Goals By Club', x=df['Club'][0:size], y=df['average_taken_goals'][0:size]), row=1, col=1)
        fig.add_trace(go.Scatter(name='Average Goal Diff By Club', x=df['Club'][0:size], y=df['diff'][0:size]), row=1, col=1)
        fig.update_layout(barmode='group')

        fig.add_trace(go.Table(columnwidth=[35, 35, 35, 35, 35],
                                        header=dict(values=['Club', 'Total Goals', 'Total Taken Goals',
                                        'Total Goal Difference', 'Average Points by Edition']),
                                        cells=dict(values=[df.Club[0:size], df.total_goals[0:size],
                                                           df.total_taken_goals[0:size], df.total_diff[0:size],
                                                           df.average_points[0:size]])), row=2, col=1)
        fig.update_layout(
            height=1000,
            title_text="Best team of : " + str(ligue),
        )

    else:

        # get data that we want from MongoDB database
        strongest_clubs = db[ligue].aggregate([{"$group" : {"_id" : "$HomeTeam",
        "average_goals_by_clubs" : {"$avg" : "$FTHG"},
        "average_taken_goals_by_clubs" : {"$avg" : "$FTAG"},
        "total_goals_by_clubs" : {"$sum" : "$FTHG"},
        "total_taken_goals_by_clubs" : {"$sum" : "$FTAG"},
        "average_odds_by_clubs" : {"$avg" : "$BbAvH"} }}])

        # create dataframe and new columns
        df = []
        for x in strongest_clubs:
            df.append([x['_id'], x['average_goals_by_clubs'], x['average_taken_goals_by_clubs'], x['average_odds_by_clubs'],
            x['total_goals_by_clubs'], x['total_taken_goals_by_clubs']])
        df = pd.DataFrame(df, columns = ['Club', 'Average_Goals_By_Club', 'Average_Taken_Goals_By_Club', 'average_odds_by_clubs',
        'total_goals_by_clubs', 'total_taken_goals_by_clubs'])

        df['diff'] = df['Average_Goals_By_Club'] - df['Average_Taken_Goals_By_Club']
        df['total_diff'] = df['total_goals_by_clubs'] - df['total_taken_goals_by_clubs']
        df['average_odds_by_clubs'] = df['average_odds_by_clubs'].round(2)
        df = df.sort_values(by=['diff'], ascending=False)
        
        # create figure
        fig = make_subplots(rows=2, cols=1, vertical_spacing=0.1, specs=[[{"type": "bar"}],[{"type": "table"}]])
        fig.add_trace(go.Bar(name='Average Goals By Club', x=df['Club'][0:size], y=df['Average_Goals_By_Club'][0:size]), row=1, col=1)
        fig.add_trace(go.Bar(name='Average Taken Goals By Club', x=df['Club'][0:size], y=df['Average_Taken_Goals_By_Club'][0:size]), row=1, col=1)
        fig.add_trace(go.Scatter(name='Average Goals Diff By Club', x=df['Club'][0:size], y=df['diff'][0:size]), row=1, col=1)
        fig.update_layout(barmode='group')

        fig.add_trace(go.Table(columnwidth=[35, 35, 35, 35, 35],
                                        header=dict(values=['Club', 'Total Goals', 'Total Taken Goals',
                                        'Total Goal Difference', 'Average Odds']),
                                        cells=dict(values=[df.Club[0:size], df.total_goals_by_clubs[0:size],
                                                           df.total_taken_goals_by_clubs[0:size], df.total_diff[0:size],
                                                           df.average_odds_by_clubs[0:size]])), row=2, col=1)

        fig.update_layout(
            height=1000,
            title_text="Best teams of : " + str(ligue),
        )

    # encode plotly graph object so that he can be displayed in the html file
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


if __name__ == '__main__':
    # insert data into the mongodb's database and run the app
    insert_db()
    app.run(host='0.0.0.0', port=5000)
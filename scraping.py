import requests
from bs4 import BeautifulSoup
import csv

def scrap():
    
    # Champions league

    output_file = csv.writer(open('data_to_insert/championsleague.csv', 'w', encoding='utf-8'))

    output_file.writerow(['Team', 'Match_played', 'Won', 'Drawn', 'Lost', 'Goal', 'Goal_against', 'Diff', 'Pts'])

    for link in ['2102', '1656', '1551', '1555', '768', '694', '628']:

        req = requests.get(f'https://fbref.com/fr/comps/8/{link}/Stats-2018-2019-Champions-League')
        src = req.content

        soup = BeautifulSoup(src, 'html.parser')

        result_overall = soup.find(id=f'results{link}0_overall')

        results = result_overall.find_all("tr")

        for result in results:
            
            stats = result.find_all('td')

            if stats is not None and len(stats) > 0:

                if stats[0].text != '':

                    if stats[0].text[4] == ' ': Team = stats[0].text[5:]
                    else : Team = stats[0].text[4:]
                    Match_played = stats[1].text
                    Won = stats[2].text
                    Drawn = stats[3].text
                    Lost = stats[4].text
                    Goal = stats[5].text
                    Goal_against = stats[6].text
                    Diff = stats[7].text
                    Pts = stats[8].text

                    output_file.writerow([Team, Match_played, Won, Drawn, Lost, Goal, Goal_against, Diff, Pts])

    # Europa league

    output_file = csv.writer(open('data_to_insert/europaleague.csv', 'w', encoding='utf-8'))

    output_file.writerow(['Team', 'Match_played', 'Won', 'Drawn', 'Lost', 'Goal', 'Goal_against', 'Diff', 'Pts'])

    for link in ['2103', '1657', '1552', '801', '769', '695', '629']:

        req = requests.get(f'https://fbref.com/fr/comps/8/{link}/Stats-2018-2019-Europa-League-Stats')
        src = req.content

        soup = BeautifulSoup(src, 'html.parser')

        result_overall = soup.find(id=f'results{link}0_overall')

        results = result_overall.find_all("tr")

        for result in results:
            
            stats = result.find_all('td')

            if stats is not None and len(stats) > 0:

                if stats[0].text != '':

                    if stats[0].text[4] == ' ': Team = stats[0].text[5:]
                    else : Team = stats[0].text[4:]
                    Match_played = stats[1].text
                    Won = stats[2].text
                    Drawn = stats[3].text
                    Lost = stats[4].text
                    Goal = stats[5].text
                    Goal_against = stats[6].text
                    Diff = stats[7].text
                    Pts = stats[8].text

                    output_file.writerow([Team, Match_played, Won, Drawn, Lost, Goal, Goal_against, Diff, Pts])

scrap()
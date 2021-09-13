import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import numpy as np

# Set up credentials for web scraping
headers = {'User-Agent': 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

years = [i for i in range(2014, 2021)]
weeks = [i for i in range(1, 20)]


# Main scraping method for obtaining data
def scrape():
    pass

def standardize_team_name(name):
    name = re.sub(r'\([^)]*\)', '', name)
    name = name.replace(' ', '-').lower()
    name = re.sub(r'(-)+', r'\1', name)
    if name[-1] == "-":
        name = name[: len(name)-1]
    return name

# Standardizes a given name
# e.g. "Andrew Carter" -> "andrew-carter"
def standardize_name(name):
    name = re.sub(r'[^A-Za-z0-9 ]+', '', name)
    name = name.replace(' ', '-').lower()
    return name

# Extracts tangible data for pollster names from HTML source code
def extract_name_data(df):
    url = 'https://collegepolltracker.com/basketball/pollsters/'
    for year in years:
        i = 0
        page = requests.get(url + str(year), headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all("span", {"class": "pollsterRankName"})
        for result in results:
            if year is years[0]:
                df = df.append({year: standardize_name(result.text)}, ignore_index=True)
            else: 
                df.loc[i, year] = standardize_name(result.text)
            i+=1

    return df

def extract_team_data(pollster_df, team_df):
    url = 'https://collegepolltracker.com/basketball/pollster/'
    for year in years: # represents a single year
        teams = []
        for i in range(0, 67):
            for week in weeks:
                i=0
                week_var = week

                if week_var == 0:
                    week_var = "pre-season"
                elif week_var == 19:
                    week_var = "final-rankings"

                page = requests.get(url + str(names_df.at[i, year])+'/'+str(year)+'/'+str(week_var), headers = headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                results = soup.find_all("span", {"class": "teamName"})

                for result in results:
                    if result.text not in teams:
                        if year is years[0]:
                            team_df = team_df.append({year: standardize_name(result.text)}, ignore_index=True)
                        else: 
                            team_df.loc[i, year] = standardize_name(result.text)
                        i+=1
                        teams.append(result.text)

    return team_df

def extract_ballot_data(ballot_df):
    url = 'https://collegepolltracker.com/basketball/pollster/'
    row = 0
    for year in years:
        for i in range(0, 67):
            pollster_name = str(names_df.at[i, year])
            if pollster_name != "nan":
                for week in weeks:
                    week_var = week

                    if week_var == 1:
                        week_var = "pre-season"
                    elif week_var == 19:
                        week_var = "final-rankings"
                    else:
                        week_var = "week-"+str(week)

                    page = requests.get(url + str(names_df.at[i, year])+'/'+str(year)+'/'+str(week_var), headers = headers)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    results = soup.find_all("span", {"class": "teamName"})
                    
                    ballot_df = ballot_df.append({"season": year, "week": week, "pollster": pollster_name}, ignore_index=True)

                    count = 1
                    for result in results:
                        if count <= 25:
                            ballot_df.loc[row, count] = standardize_team_name(result.text)
                            count+=1
                    row+=1

    return ballot_df


# Create auxiliary files for all pollster names
names_df = pd.DataFrame(columns=years)
names_df = extract_name_data(names_df)
names_df.to_csv('names.csv')

# Create auxiliary files for all teams ballotted at least once
teams_df = pd.DataFrame(columns=years)
teams_df = extract_team_data(names_df, teams_df)
teams_df.to_csv('teams.csv')

# Main CSV file for all webscraped ballot data
ballot_columns = [i for i in range(1, 26)]
ballot_columns.insert(0, "pollster")
ballot_columns.insert(0, "week")
ballot_columns.insert(0, "season")
ballots_df = pd.DataFrame(columns=ballot_columns)
ballots_df = extract_ballot_data(ballots_df)
ballots_df.to_csv('ballots.csv')



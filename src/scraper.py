import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set up credentials for web scraping
headers = {'User-Agent': 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

years = [i for i in range(2014, 2021)]
weeks = [i for i in range(1, 20)]


# Main scraping method for obtaining data
def scrape():
    pass

# Standardizes a given name
# e.g. "Andrew Carter" -> "andrew-carter"
def standardize_name(name):
    return name.replace(' ', '-').lower()

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


# Create auxiliary files for all pollster names
names_df = pd.DataFrame(columns=years)
names_df = extract_name_data(names_df)
names_df.to_csv('names.csv')

# Create auxiliary files for all teams ballotted at least once
teams_df = pd.DataFrame(columns=years)
teams_df = extract_team_data(names_df, teams_df)
teams_df.to_csv('teams.csv')



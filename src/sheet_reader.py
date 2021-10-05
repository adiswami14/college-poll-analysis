import pandas as pd
import re
import numpy as np
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


headers = {'User-Agent': 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

weeks = [i for i in range(1, 20)]
names_df = pd.read_csv('names.csv')
ballots_df = pd.read_csv('ballots.csv')
teams_df = pd.read_csv('teams.csv')

def get_ranking(team, week, year):
    ranking_dict = {}
    for pollster in names_df[str(year)]:
        if pollster != "nan":
            ext_df = ballots_df.loc[(ballots_df["season"] == year) & (ballots_df["pollster"] == pollster) & (ballots_df["week"] == week)]
            if team in ext_df.values:
                for (column_name, column_data) in ext_df.iteritems():
                    if column_data.values[0] == team:
                        ranking_dict[pollster] = int(column_name)

    return pd.DataFrame([ranking_dict])

def strip_date(s):
    return s[s.find("(")+1:s.find(")")]

def set_df(df, filename):
    df = pd.read_excel(filename)
    return df

def find_winning_probability(money_line):
    prob = None

    if money_line == "NL":
        prob = 0.5
    else:
        try:
            money_line = int(money_line)
            if money_line >= 0:
                prob = 100/(100+money_line)
            else:
                prob = abs(money_line)/(100+abs(money_line))
        except:
            prob = 0.5

    return prob

def standardize_camelCase_name(name):
    if name.isupper() and name.isalpha():
        return name.lower()
    new_name = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
    return new_name

def check_win(df):
    for i, score in enumerate(df['Final']):
        if i%2==0:
            if df.loc[i, 'Final'] < df.loc[i+1, 'Final']:
                df.loc[i, 'Result'] = 'L'
                df.loc[i+1, 'Result'] = 'W'
            elif df.loc[i, 'Final'] > df.loc[i+1, 'Final']:
                df.loc[i, 'Result'] = 'W'
                df.loc[i+1, 'Result'] = 'L'
            else:
                df.loc[i, 'Result'] = 'T'
                df.loc[i+1, 'Result'] = 'T'

    return df

def get_week_dict(year):
    url = 'https://collegepolltracker.com/basketball/'
    week_dict = {}
    for week in weeks:
        week_var = week

        if week_var == 1:
            week_var = "pre-season"
        elif week_var == 19:
            week_var = "final-rankings"
        else:
            week_var = "week-"+str(week)

        try:
            page = requests.get(url +str(year)+'/'+str(week_var), headers = headers)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find_all("span", {"class": "weekBar"})

            for result in results:
                date = datetime.strptime(strip_date(result.text), '%b %d, %Y')
                d_range = None
                if week == 1:
                    d_range = 14
                else:
                     d_range = 7
                date_list = [date + timedelta(days=x) for x in range(d_range)]
                week_dict[week] = [d.strftime("%m/%d") for d in date_list]
        except ConnectionError as e: 
            pass

    return week_dict

def get_week(date, week_dict):
    date = str(date)
    if len(date) == 3:
        date = "0"+date
    date_str = date[:len(date)//2]+"/"+date[len(date)//2:len(date)]
    for week in weeks:
        if date_str in week_dict[week]:
            return week
    
    if date[:len(date)//2] == "11":
        return 1
    else:
        return 19
        
        
def create_csv_file(input_path: str, output_path : str, year: str):
    df = pd.DataFrame()
    df = set_df(df, input_path)

    df = df.drop(columns=['Rot', '1st', '2nd', 'Open', 'Close', '2H'], axis = 1)
    df['Probability'] = df['ML'].apply(find_winning_probability)
    df['Team'] = df['Team'].apply(standardize_camelCase_name)

    week_dict = get_week_dict(year)

    df['Week'] = df.apply(lambda x: get_week(x['Date'], week_dict), axis=1)

    df = check_win(df)

    copy_df = pd.DataFrame(df)
    for index, row in df.iterrows():
        if row['Team'] not in list(teams_df[str(year)].to_numpy()):
            copy_df = copy_df.drop(index)

    df = pd.DataFrame(copy_df)
    df = df.reset_index()

    ranking_df = pd.DataFrame()
    for index, row in df.iterrows():
        ranking_df = ranking_df.append(get_ranking(row['Team'], row['Week'], year), ignore_index=True)


    df = pd.concat([df, ranking_df], axis =1)

    df.to_csv(output_path)

create_csv_file('spreadsheets/2014-15.xlsx', 'seasons/2014-15.csv', 2014)
create_csv_file('spreadsheets/2015-16.xlsx', 'seasons/2015-16.csv', 2015)
create_csv_file('spreadsheets/2016-17.xlsx', 'seasons/2016-17.csv', 2016)
create_csv_file('spreadsheets/2017-18.xlsx', 'seasons/2017-18.csv', 2017)
create_csv_file('spreadsheets/2018-19.xlsx', 'seasons/2018-19.csv', 2018)
create_csv_file('spreadsheets/2019-20.xlsx', 'seasons/2019-20.csv', 2019)


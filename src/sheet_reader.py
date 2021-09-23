import pandas as pd
import re
import numpy as np

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
        
        
def create_csv_file(input_path: str, output_path : str):
    df = pd.DataFrame()
    df = set_df(df, input_path)

    df = df.drop(columns=['Rot', '1st', '2nd', 'Open', 'Close', '2H'], axis = 1)
    df['Probability'] = df['ML'].apply(find_winning_probability)
    df['Team'] = df['Team'].apply(standardize_camelCase_name)

    df = check_win(df)
    df.to_csv(output_path)

create_csv_file('spreadsheets/2014-15.xlsx', 'seasons/2014-15.csv')
create_csv_file('spreadsheets/2015-16.xlsx', 'seasons/2015-16.csv')
create_csv_file('spreadsheets/2016-17.xlsx', 'seasons/2016-17.csv')
create_csv_file('spreadsheets/2017-18.xlsx', 'seasons/2017-18.csv')
create_csv_file('spreadsheets/2018-19.xlsx', 'seasons/2018-19.csv')
create_csv_file('spreadsheets/2019-20.xlsx', 'seasons/2019-20.csv')
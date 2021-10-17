import pandas as pd
import numpy as np
from borda_count import BordaCount

def output_to_file(week, season, weights):
    next_year = (season-2000)+1
    df = pd.read_csv('seasons/'+str(season)+'-'+str(next_year)+'.csv')
    df = df.loc[df["Week"] == week]
    df = df.iloc[::-1]
    df = df.drop_duplicates(['Team'])
    df = df.head(25)

    bc_list = []
    diff_list = []

    for index, row in df.iterrows():
        list_row = row.tolist()
        list_row = list_row[11:]
        list_row = [0 if np.isnan(val) else int(val) for val in list_row]
        bc = BordaCount(weights, list_row)
        bc_list.append(bc.get_aggregate_value())
    
    df['Standard Rank'] = [i for i in range(1, 26)]

    copy_list = list(bc_list)
    copy_list.sort()
    copy_list.reverse()

    df["Adjusted Rank"] = [copy_list.index(i)+1 for i in bc_list]
    df = df.reset_index()
    df = df[['Team', 'Week' ,'Standard Rank', 'Adjusted Rank']]

    for index, row in df.iterrows():
        diff_list.append(int(row['Standard Rank']) - int(row['Adjusted Rank']))

    df['Ranking Change'] = diff_list

    df.to_csv('comparator.csv')


output_to_file(17, 2018, [45 for i in range(25)])
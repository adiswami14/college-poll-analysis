import pandas as pd
import numpy as np


def process_percentage_from_file(filename):
    file_df = pd.read_csv(filename)
    file_df = file_df.T
    file_df = file_df.drop(['Unnamed: 0', 'Weights'], axis = 0)
    file_df = file_df.fillna(0)
    percentage_list = []
    for i in range(10):
        percentage_list.append((np.count_nonzero(file_df[i]))/(file_df.shape[0]))
    return percentage_list

dowdall_list = process_percentage_from_file('data/dowdall_fixed.csv')
formula_list = process_percentage_from_file('data/formula.csv')
top_list = process_percentage_from_file('data/top-n/top10.csv')


dic = {'Dowdall': dowdall_list, 'Formula 1': formula_list, 'Top 10': top_list}
output_df = pd.DataFrame(data=dic)
output_df.to_csv('data/percentages.csv')


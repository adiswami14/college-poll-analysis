import pandas as pd
import numpy as np
from borda_count import BordaCount

def weighted_borda(week, season, weights):
    next_year = (season-2000)+1
    df = pd.read_csv('data/game-results/'+str(season)+'-'+str(next_year)+'.csv')
    df = df.loc[df["Week"] == week]
    df = df.iloc[::-1]
    df = df.drop_duplicates(['Team'])
    df = df.head(25)

    range_len = 0
    if (df.shape)[0] > 25:
        range_len = 25
    else:
        range_len = df.shape[0]
    
    bc_list = []
    diff_list = []

    for index, row in df.iterrows():
        list_row = row.tolist()
        list_row = list_row[11:]
        list_row = [0 if np.isnan(val) else int(val) for val in list_row]
        bc = BordaCount(weights, list_row)
        bc_list.append(bc.get_aggregate_value())
    
    df['Standard Rank'] = [i for i in range(1, range_len+1)]

    copy_list = list(bc_list)
    copy_list.sort()
    copy_list.reverse()

    adj_list = [0 for i in range(range_len)]
    if len(bc_list) > 0:
        adj_list = [copy_list.index(i)+1 for i in bc_list]
    df["Adjusted Rank"] = adj_list
    df = df.reset_index()
    df = df[['Team', 'Week' ,'Standard Rank', 'Adjusted Rank']]

    for index, row in df.iterrows():
        diff_list.append(int(row['Standard Rank']) - int(row['Adjusted Rank']))

    df['Ranking Change'] = diff_list
    return diff_list
    # df.to_csv('comparator.csv')

def loop_over_borda(output_path: str, weights):
    df = pd.DataFrame()
    df["Weights"] = weights
    for season in range(2014, 2020):
        for week in range(1, 20):
            print(str(season)+"\t"+str(week))
            borda_list = weighted_borda(week, season, weights)
            # for i in range(len(borda_list), df.shape[0]):
            #     borda_list.append("N/A")
            df[str(season)+" "+str(week)] = borda_list
    df.to_csv(output_path)


# loop_over_borda('reverse.csv', [i for i in range(25)])
# loop_over_borda('dowdall.csv', [1/i for i in range(1, 26)])

# formula_one_list = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
# for i in range(15):
#     formula_one_list.append(0)
# loop_over_borda('formula.csv', formula_one_list)

# for n in range(1,11):
#     l = [n - i if i < n else 0 for i in range(25)]
#     loop_over_borda('top-n/top'+str(n)+'.csv', l)
# college-poll-analysis
A project that analyzes AP College Poll Data for college football.

This is a guide to understand all of the files in the `data` folder.

The `raw-data` folder contains the data on each of the seasons from 2014-15 to 2019-20 from the original website we webscraped from.

This raw data has a corresponding counterpart in the `game-results` folder, where each file represents its seasonal namesake. The files in this folder are processed and filtered versions of those in the `raw-data` folder, containing all the results of each game for each team, along with the money line for each game.

The `processed-data` folder contains three files. The first is `ballots.csv`, which is the all-encompassing file that is the fruit of all the webscraping done. In this file, each row represents a ballot, with columns representing the week, season, pollster, and the rankings from 1-25. The next file is `pollster_names.csv`, which contains all the pollsters for each season. This file is for data validation and testing. The same goes for `teams.csv`, which has all the teams present in at least one ballot, with each column representing a season.

The other data represents the weighted Borda tests. The `top-n` folder contains ten CSV files, each which corresponds to what would happen if we were to tamper with the standard Borda count, by taking only the **top n** rankings to have a nonzero value, and zeroing out the rest of the weighting vector. 

The same for `dowdall.csv`, `formula.csv`, and `reverse.csv`, all which represent the rankings change that would occur if the standard Borda count we employ were to be changed to the weight vector passed into the file. 

The last two files are the `formula-teams.csv` and `dowdall-teams.csv`, each which represent the top 25 teams (according to the standard Borda count) in the ranking for a given season and week, just for a reference when looking at which teams changed rankings.
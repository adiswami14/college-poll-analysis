import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set up credentials for web scraping
headers = {'User-Agent': 
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}

years = [i for i in range(2013, 2021)]
weeks = [i for i in range(1, 20)]


# Main scraping method for obtaining data
def scrape():
    pass

# Standardizes a given name
# e.g. "Andrew Carter" -> "andrew-carter"
def standardize_name(name):
    return name.replace(' ', '-').lower()

# Extracts tangible data from HTML source code
def extract_data(df):
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

names_df = pd.DataFrame(columns=years)
names_df = extract_data(names_df)
print(names_df)
names_df.to_csv('names.csv')

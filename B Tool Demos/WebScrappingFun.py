import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
import tweepy

url = "https://www.allmysportsteamssuck.com/ncaa-division-i-football-and-basketball-twitter-hashtags-and-handles/"


def scrape_team_twitter_info():
    response = requests.get(url)

    if response.status_code == 200:
        # make sure the status code is okay
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup)
        table = soup.find("table", attrs={"id": "rankingstable"})
        # print(table)
        thead = table.find("thead")
        # print(thead)
        ths = thead.find_all("th")
        col_names = [th.get_text() for th in ths]
        # print(col_names)

        # try to parse the tbody
        tbody = table.find("tbody")
        # print(tbody)
        trs = tbody.find_all("tr")
        rows = []
        for tr in trs:
            row = []
            tds = tr.find_all("td")
            for td in tds:
                row.append(td.get_text())
            rows.append(row)
        df = pd.DataFrame(rows, columns=col_names)
        df = df.set_index("School")
        return df
    return None

def fetch_user_account_info(client, username):
    response = client.get_user(username=username, user_fields=["created_at", "public_metrics"])
    print(type(response.data))
    user = response.data
    print(user.keys())
    values = {"user_id": user.id, "username": user.username, "created_at": user.created_at}
    values.update(user.public_metrics)
    ser = pd.Series(values)
    return ser

if __name__ == "__main__":
    # df = scrape_team_twitter_info()
    # print(df)
    # df.to_csv("team_twitter_info.csv")

    df = pd.read_csv("team_twitter_info.csv", index_col=0)
    # print(df)

    # setting up twitter API
    with open("twitter_keys.json") as infile:
        json_obj = json.load(infile)
        token = json_obj["bearer_token"]
        # pip install tweepy needed for this step
        client = tweepy.Client(bearer_token=token)
    
    # client is still in scope out of the with statement
    # lets first request data about a single twitter account
    zag_username = df.loc["Gonzaga", "Men’s Basketball Team"][1:]
    print(zag_username)
    user_ser = fetch_user_account_info(client, zag_username)
    print(user_ser)
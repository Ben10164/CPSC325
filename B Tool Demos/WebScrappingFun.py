import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.allmysportsteamssuck.com/ncaa-division-i-football-and-basketball-twitter-hashtags-and-handles/"

def scrape_team_twitter_info():
    response = requests.get(url)
    
    print(response.status_code)
    print(response.text)

if __name__ == "__main__":
    scrape_team_twitter_info()
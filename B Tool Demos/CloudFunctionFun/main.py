import os
from datetime import datetime, timezone, timedelta
import pandas as pd
import tweepy
from google.cloud import bigquery

DATASET_ID = "twitter_dataset"
TABLE_ID = "tweets"

def insert_rows_to_bq(rows):
    client = bigquery.Client() # searches for credentials in an environment variable
    dataset_ref = client.dataset(DATASET_ID)
    table_ref = dataset_ref.table(TABLE_ID)
    errors = client.insert_rows_jason(table_ref, rows)
    if len(errors) == 0:
        print("Successfully inserted rows")
    else:
        print("Errors inserting rows:", errors)

def fetch_recent_tweets_for_user(client, user_id, start_time):
    response = client.get_users_tweets(user_id, tweet_fields = ["created_at"], start_time=start_time)
    rows = []

    if response.data is not None:
        for tweet in response.data:
            # print(tweet)
            created_at = pd.Timestamp(tweet.created_at).strftime("%Y-%m-%d %H::%M:%S")
            values = {"tweet_id": tweet.id, "author_id": user_id, "created_at": created_at, "text": tweet.text}
            rows.append(values)
    return rows

def entry_point(request): # request is a Flask request
    # we can ignore request (cloud schedule won't be putting anything in it)
    user_id = 602989093
    bearer_token = os.environ.get("BEARER_TOKEN")
    client = tweepy.Client(bearer_token=bearer_token)

    start_time = datetime.now(timezone.utc) - timedelta(hours=24)
    start_time = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")

    tweet_rows = fetch_recent_tweets_for_user(client, user_id, start_time)
    print(tweet_rows)

    # insert tweet_rows into a bigquery table
    insert_rows_to_bq(tweet_rows)

    return "Success", 200

if __name__ == "__main__":
    entry_point(None)


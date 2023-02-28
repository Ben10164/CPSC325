import os
import json
import tweepy
import pandas as pd
from google.cloud import pubsub

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_keys.json"

TOPIC_PATH = "projects/eternal-ship-376417/topics/tweets"


class TweetStreamer(tweepy.StreamingClient):
    def __init__(self, bearer_token):
        super().__init__(bearer_token=bearer_token,
                         wait_on_rate_limit=True)

    def clear_and_set_filter_rules(self, filter_terms):
        # clear out any existing rules
        response = self.get_rules()
        if response.data is not None:
            rule_ids = [rule.id for rule in response.data]
            self.delete_rules(rule_ids)
        rules = [tweepy.StreamRule(term) for term in filter_terms]
        print(rules)
        response = self.add_rules(rules)
        print("added number of rules:", len(response.data))

    def on_connect(self):
        print("Connection successful")

    def on_disconnect(self):
        print("Connection disconnected")

    def on_tweet(self, tweet):
        created_at = pd.Timestamp(
            tweet.created_at).strftime("%Y-%m-%d %H::%M:%S")
        values = {"tweet_id": tweet.id, "author_id": tweet.author_id,
                  "created_at": created_at, "text": tweet.text}
        print(values)
        publish_tweet(values)


def publish_tweet(tweet_dict):
    # need to pip install google-cloud-pubsub and import it
    publisher_client = pubsub.PublisherClient()  # this code is
    # going to authenticate with google_keys.json
    tweet_str = json.dumps(tweet_dict).encode("utf-8")
    future = publisher_client.publish(TOPIC_PATH, tweet_str)
    print("published:", future.result())


if __name__ == "__main__":
    with open("twitter_keys.json") as infile:
        json_obj = json.load(infile)
        token = json_obj["bearer_token"]

    streamer = TweetStreamer(token)
    # with essential access (free tier), we can have
    # 5 filter terms/rules
    filter_terms = ["from:ZagMBB", "from:GinaSprint"]  # can put user ID
    streamer.clear_and_set_filter_rules(filter_terms)
    # start the streamer
    streamer.filter(tweet_fields=["created_at", "author_id"])

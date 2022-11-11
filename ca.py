import requests
import pandas as pd
import argparse
import calendar
import time

parser = argparse.ArgumentParser()
parser.add_argument('--user', type=str, required=True)
args = parser.parse_args()

timestamp = calendar.timegm(time.gmtime())
user = args.user
url = "https://curiouscat.live/api/v2.1/profile"
querystring = {"username": user, "count": 100}
response = requests.request("GET", url, params=querystring)
data = response.json()
posts = []
posts.extend([i["post"] for i in data["posts"]])

print("Downloading...")
while True:
    querystring = {"username": user,
                   "max_timestamp": posts[-1]["timestamp"], "count": 100}
    response = requests.request("GET", url, params=querystring)
    data = response.json()
    posts.extend([i["post"] for i in data["posts"][1:]])
    if len(data["posts"]) < 100:
        break



def select_fields(dict):
    keys = ['id', 'comment', 'reply', "timestamp"]
    new_dict = {x: dict[x] for x in keys}
    return new_dict


answers = list(map(select_fields, posts))

answers_df = pd.DataFrame(answers)
answers_df["timestamp"] = pd.to_datetime(answers_df['timestamp'], unit='s')
answers_NoDublicates_df = answers_df.drop_duplicates(subset=["id"], keep="first")
print(f"{len(answers_NoDublicates_df)} Answers Saved As {user}-{timestamp}.csv")
fileName = f"{user}-{timestamp}.csv"
answers_NoDublicates_df.to_csv(fileName, sep=',', index=False)


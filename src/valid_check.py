import sys
from datetime import date, datetime, timedelta, timezone
from glob import glob

import pandas as pd
from dateutil.relativedelta import relativedelta

from twitter_api_connect import connect_to_endpoint, waitUntilReset


def get_id(BT, username):
    url = "https://api.twitter.com/2/users/by"
    params1 = {"usernames": "{}".format(username), "user.fields": "id"}
    headers = {"Authorization": "Bearer {}".format(BT)}
    response, json_response = connect_to_endpoint(url, params1, headers)

    if int(response.headers["x-rate-limit-remaining"]) == 0:
        waitUntilReset(response.headers["x-ratelimit-reset"])

    id = json_response["data"][0]["id"]

    return id

def follow_check(BT, id):
    party_list = glob(
        "/home/tmasukawa/OpinionAnalysis/mp_account_list/*.csv"
    )

    url = "https://api.twitter.com/2/users/{}/following".format(id)
    params = {"max_results": "1000"}
    headers = {"Authorization": "Bearer {}".format(BT)}

    followings = []

    while True:
        response, json_response = connect_to_endpoint(url, params, headers)
        followings += json_response["data"]

        if int(response.headers["x-rate-limit-remaining"]) == 0:
            waitUntilReset(response.headers["x-ratelimit-reset"])

        if ("next_token" in json_response["meta"]):
            params["pagination_token"] = json_response["meta"]["next_token"]
        else:
            break

    json_followings = pd.json_normalize(followings)

    for party in party_list:
        csv = pd.read_csv(party, encoding="utf-8")

        for member in csv["account"]:
            if member in json_followings["username"].values:
                return True
            else:
                continue

    print("Not following Diet Member's account.", file=sys.stderr)
    return False


def active_check(BT, id, string, pre_datetime):
    url2 = "https://api.twitter.com/2/users/{}/tweets/".format(id)
    params2 = {
        "tweet.fields": "author_id,created_at,public_metrics,text",
        "expansions": "author_id,referenced_tweets.id",
        "user.fields": "description,created_at,public_metrics",
        "exclude": "retweets",
        "max_results": "40",#念のため40
    }
    headers = {"Authorization": "Bearer {}".format(BT)}

    response, json_response = connect_to_endpoint(url2, params2, headers)

    if int(response.headers["x-rate-limit-remaining"]) == 0:
        waitUntilReset(response.headers["x-ratelimit-reset"])

    today = date.today()
    one_month_ago = today - relativedelta(days=30)

    create_at_full = json_response["includes"]["users"][0]["created_at"].split("T")
    create_at_date = datetime.strptime(create_at_full[0], "%Y-%m-%d")
    create_at = date(create_at_date.year, create_at_date.month, create_at_date.day)

    if date(2022,1,1) <= create_at:
        print("After 2022/1/1.", create_at, file=sys.stderr)
        return False

    if int(json_response["includes"]["users"][0]["public_metrics"]["tweet_count"]) <= (today-create_at).days * 0.34:
        print("Once every 3 days",json_response["includes"]["users"][0]["public_metrics"]["tweet_count"], file=sys.stderr)
        return False

    if len(json_response["data"]) >= 10:
        tweet_date = json_response["data"][9]["created_at"].split("T")
        check_datetime = datetime.strptime(tweet_date[0], "%Y-%m-%d")
        check_date = date(check_datetime.year, check_datetime.month, check_datetime.day)
        if check_date <= one_month_ago:
            print("30days Check", check_date, file=sys.stderr)
            return False
    else:
        print("Not over 10 tweets",len(json_response["data"]), file=sys.stderr)
        return False

    post = json_response["data"][0]["text"]
    post_time = json_response["data"][0]["created_at"].replace(".000Z", "")

    datetime_utc = datetime.strptime(post_time, "%Y-%m-%dT%H:%M:%S")
    datetime_jst = datetime_utc + timedelta(hours=9)

    if string in post:
        if pre_datetime - timedelta(seconds=70) <= datetime_jst <= pre_datetime:
            return True
        else:
            print("Post is not in time", pre_datetime - timedelta(seconds=70), datetime_jst, pre_datetime, file=sys.stderr)
            return False
    else:
        print("Not String", string, file=sys.stderr)
        return False

def active_check_not_string(BT, id):
    url2 = "https://api.twitter.com/2/users/{}/tweets/".format(id)
    params2 = {
        "tweet.fields": "author_id,created_at,public_metrics,text",
        "expansions": "author_id,referenced_tweets.id",
        "user.fields": "description,created_at,public_metrics",
        "exclude": "retweets",
        "max_results": "40",#念のため40
    }
    headers = {"Authorization": "Bearer {}".format(BT)}

    response, json_response = connect_to_endpoint(url2, params2, headers)

    if int(response.headers["x-rate-limit-remaining"]) == 0:
        waitUntilReset(response.headers["x-ratelimit-reset"])

    today = date.today()
    one_month_ago = today - relativedelta(days=30)

    create_at_full = json_response["includes"]["users"][0]["created_at"].split("T")
    create_at_date = datetime.strptime(create_at_full[0], "%Y-%m-%d")
    create_at = date(create_at_date.year, create_at_date.month, create_at_date.day)

    if date(2022,1,1) <= create_at:
        print("After 2022/1/1.", create_at, file=sys.stderr)
        return False

    if int(json_response["includes"]["users"][0]["public_metrics"]["tweet_count"]) <= (today-create_at).days * 0.34:
        print("Once every 3 days",json_response["includes"]["users"][0]["public_metrics"]["tweet_count"], file=sys.stderr)
        return False

    if len(json_response["data"]) >= 10:
        tweet_date = json_response["data"][9]["created_at"].split("T")
        check_datetime = datetime.strptime(tweet_date[0], "%Y-%m-%d")
        check_date = date(check_datetime.year, check_datetime.month, check_datetime.day)
        if check_date <= one_month_ago:
            print("30days Check", check_date, file=sys.stderr)
            return False
    else:
        print("Not Over 10 Tweets",len(json_response["data"]), file=sys.stderr)
        return False

    return True

def active_check_only_string(BT, id, string, pre_datetime):
    url2 = "https://api.twitter.com/2/users/{}/tweets/".format(id)
    params2 = {
        "tweet.fields": "author_id,created_at,public_metrics,text",
        "expansions": "author_id,referenced_tweets.id",
        "user.fields": "description,created_at,public_metrics",
        "exclude": "retweets",
        "max_results": "40",#念のため40
    }
    headers = {"Authorization": "Bearer {}".format(BT)}

    response, json_response = connect_to_endpoint(url2, params2, headers)

    if int(response.headers["x-rate-limit-remaining"]) == 0:
        waitUntilReset(response.headers["x-ratelimit-reset"])

    post = json_response["data"][0]["text"]
    post_time = json_response["data"][0]["created_at"].replace(".000Z", "")

    datetime_utc = datetime.strptime(post_time, "%Y-%m-%dT%H:%M:%S")
    datetime_jst = datetime_utc + timedelta(hours=9)


    post = post.replace("\n", "")
    print(post, file=sys.stderr)
    
    if string in post:
        return True
        # if pre_datetime - timedelta(seconds=70) <= datetime_jst <= pre_datetime:
        #     return True
        # else:
        #     print("Post is not in time", pre_datetime - timedelta(seconds=70), datetime_jst, pre_datetime, file=sys.stderr)
        #     return False
    else:
        print("Not String", string, file=sys.stderr)
        return False

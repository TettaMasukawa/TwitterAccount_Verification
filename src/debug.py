from twitter_api_connect import connect_to_endpoint, waitUntilReset


def get_data(BT, username):
    url = "https://api.twitter.com/2/users/by"
    params1 = {
        "usernames": "{}".format(username),
        "post.fields": "author_id,created_at,public_metrics,text",
        "expansions": "author_id,referenced_posts.id",
        "user.fields": "description,created_at,public_metrics",
        "exclude": "reposts",
        "max_results": "40",
    }
    headers = {"Authorization": "Bearer {}".format(BT)}
    response, json_response = connect_to_endpoint(url, params1, headers)

    if int(response.headers["x-rate-limit-remaining"]) == 0:
        waitUntilReset(response.headers["x-rate-limit-reset"])
        
    try:
        id = json_response["data"]
    except:
        return "NA"

    return id

if __name__ == "__main__":
    BT = "AAAAAAAAAAAAAAAAAAAAAD%2FJPQEAAAAA7%2BNdrLam%2FkVdRcU3%2B6I5tA6I8Ic%3DljqTXJKdge7Uid3JlwgKsalU2xFBXlrq9Wzpe09xF2azv0rKvB"
    
    data = get_data(BT, "ChiffonF31")
    print(data)

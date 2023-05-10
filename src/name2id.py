import pandas as pd

from twitter_api_connect import connect_to_endpoint, waitUntilReset


def get_id(BT, username):
    url = "https://api.twitter.com/2/users/by"
    params1 = {"usernames": "{}".format(username), "user.fields": "id"}
    headers = {"Authorization": "Bearer {}".format(BT)}
    response, json_response = connect_to_endpoint(url, params1, headers)

    if int(response.headers["x-rate-limit-remaining"]) == 0:
        waitUntilReset(response.headers["x-rate-limit-reset"])
        
    try:
        id = json_response["data"][0]["id"]
    except:
        return "NA"

    return id

if __name__ == "__main__":
    BT = "AAAAAAAAAAAAAAAAAAAAAC%2FlQgEAAAAAi9yH0D1YnXy%2F4tKDFNd4Jw%2B9GyQ%3DukHqkVzZWJQX48nwMVys5VglneLIRW3CG566Z0ZY8SUCBkGPsa"
    # file_name = ""
    # csv = pd.read_csv(file_name, encoding="utf-8-sig")
    
    # id_list = []
    
    # for n in range(len(csv)):
    #     if pd.isna(csv["account"][n]):
    #         id_list.append("NA")
    #     else:
    #         id = get_id(BT, csv["account"][n])
    #         id_list.append(id)
        
    # csv["id"] = id_list
    
    # csv.to_csv(file_name, encoding="utf-8-sig", mode="w", index=False)
    id = get_id(BT, "Jubiloiwata_YFC")
    print(id)

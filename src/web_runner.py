import json
import sys
from datetime import datetime, timedelta, timezone

import pandas as pd
from flask import Flask, request

from valid_check import (active_check, active_check_not_string,
                         active_check_only_string, follow_check, get_id)

app = Flask(__name__)

@app.route("/debug")
def redirect_debug():
    return "接続されました。"

@app.route("/")
def redirect_func():
    username = request.args.get("username").strip("@")
    interest = "0"  # 0 or None: Only active check, 1: Active check & Follow check, 999: for debug (only identification by specified post check)
    string = request.args.get("string")
    current_date = request.args.get("currentday").replace("/", "-")
    current_time = request.args.get("currenttime")

    date_n_time = current_date + "T" + current_time

    pre_datetime = datetime.strptime(date_n_time, "%Y-%m-%dT%H:%M:%S")

    BT = ""  # Fill in BT

    id = get_id(BT, username)

    judged = pd.read_csv("../judged_account.csv", encoding="utf-8")
    account = pd.DataFrame({"account": username}, index=[1])

    # if username in judged["account"].values:
    #     return json.dumps({"valid": "あなたのアカウントは有効ではありません。"}, ensure_ascii=False)

    if interest == "1":
        if follow_check(BT, id) and active_check(BT, id, string, pre_datetime):
            account.to_csv("../judged_account.csv", encoding="utf-8", mode="a", index=False, header=False)
            return json.dumps({"valid": "あなたのアカウントは有効です。"}, ensure_ascii=False)
        else:
            return json.dumps({"valid": "あなたのアカウントは有効ではありません。"}, ensure_ascii=False)

    elif interest == "999":
        if active_check_only_string(BT, id, string, pre_datetime):
            account.to_csv("../judged_account.csv", encoding="utf-8", mode="a", index=False, header=False)
            return json.dumps({"valid": "あなたのアカウントは有効です。"}, ensure_ascii=False)
        else:
            return json.dumps({"valid": "あなたのアカウントは有効ではありません。"}, ensure_ascii=False)

    elif interest == "0" or interest == "":
        if active_check(BT, id, string, pre_datetime):
            account.to_csv("../judged_account.csv", encoding="utf-8", mode="a", index=False, header=False)
            return json.dumps({"valid": "あなたのアカウントは有効です。"}, ensure_ascii=False)
        else:
            return json.dumps({"valid": "あなたのアカウントは有効ではありません。"}, ensure_ascii=False)
    else:
        return json.dumps({"valid": "あなたのアカウントは有効ではありません。"}, ensure_ascii=False)


if __name__ == "__main__":
    app.run(debug=True, host='', port=5000) # hostにはIP Address

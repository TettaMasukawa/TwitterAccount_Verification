# TwitterAccount_Verification
Twitterアカウントがアクティブかどうかを独自の基準でチェックするシステム

## Overview
**src** : システムで使用するpythonファイルがまとめられている。  
- twitter_api_connect.py : TwitterAPIへの接続  
- valid_check : アカウントチェック  
- web_runner.py : webシステム起動

**dm_account_list_202208** : アカウントチェックで使用する国会議員リスト(随時更新予定)  

**judged_account.csv** : すでにチェックをクリアしたアカウントのリスト  

## How to Run
必要なライブラリはrequirements.txtに記載。  

バックグラウンドで実行することでwebサーバが立ち上がる。(下記参照)  
> nohup python3 web_runner.py &  

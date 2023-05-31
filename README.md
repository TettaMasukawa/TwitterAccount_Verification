# TwitterAccount_Verification
This is a system that checks whether a Twitter account is active or not based on our own criteria.  

## Overview
<pre>
.  
├── src  
│   ├── twitter_api_connect.py  
│   ├── valid_check.py  
│   └── web_runner.py  
├── requirements.txt  
└── judged_account.csv 
</pre>

**src** : Here is a collection of python files used by the system.  
- twitter_api_connect.py : Connect to Twitter API  
- valid_check : Account Validation  
- web_runner.py : Run web system

**dm_account_list_202208** : List of members of parliament used for account check (scheduled to be updated from time to time)  

**judged_account.csv** : List of accounts that have already cleared the check  

## How to Run
Required libraries are listed in 'requirements.txt'.  

You can start a web server by running it in the background.  
> nohup python3 web_runner.py &  

In this case, running logs are added to 'nohup.out'.  
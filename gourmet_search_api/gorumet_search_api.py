from itertools import count
import panads as pd
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

url = os.environ.get("GOURMET_URI")
api_key = os.environ.get("API_KEY")

params = {"key": api_key, "keyword": "福岡", "format": "json"}

res = requests.get(url, params)
res.status_code


result = res.json()

result_df = pd.DataFrame(result["results"]["shop"])


items = result["results"]["shop"]
len(items)

params = {"key": api_key, "keyword": "福岡", "format": "json", "count": 100}

import requests
import pandas as pd
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

url = os.environ.get("JSON_URI")
res = requests.get(url)

# Check the contents of the data.
df = pd.DataFrame(res.json())

# Extract specific values
body = {"id": 5}
res = requests.get(url, body)

body = {"userId": 1}
res = requests.get(url, body)
print(res.json())

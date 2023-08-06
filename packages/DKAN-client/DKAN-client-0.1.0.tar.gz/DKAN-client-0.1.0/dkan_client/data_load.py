import requests
import pandas as pd

def get_data():
    url = "https://offenedaten-koeln.de/api/action/datastore/search.json?resource_id=4b35bd42-a198-4a5a-b48b-9ba5be441833&limit=10"
    response = requests.get(url)
    return pd.DataFrame(response.json()['result']['records'])
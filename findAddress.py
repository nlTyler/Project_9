import time
import requests
import pandas as pd

def findAddress(lat, lng, key=None):
    """
    Finds the address for a tuple of latitude and longitude coordinates using the TomTom API.

    Args:
        lat (tuple): Tuple of latitudes.
        lng (tuple): Tuple of longitudes.
        key (str): API key for TomTom API. Defaults to None.

    Returns:
        pd.DataFrame: DataFrame with columns ['address', 'status_code'].
    """
    if key is None:
        key = "gTGlKsrxmGjsdTE0TN71A8wSxAM4GbCl"

    #Ensures latitude and longitude are the same length
    if isinstance(lat, tuple) and isinstance(lng, tuple):
        if len(lat) != len(lng):
            return None
    else:
        return None

    base_url = "https://api.tomtom.com/search/2/reverseGeocode/"
    results = []

    for lat_val, lng_val in zip(lat, lng):

        # Construct the query URL
        url = f"{base_url}{lat_val}%2C{lng_val}.json?key={key}&ext=JSON"

        response = requests.get(url)
        status_code = response.status_code
        time.sleep(0.1)

        # Record and return the response
        if status_code == 200:
            data = response.json()
            if "addresses" in data and data["addresses"]:
                address = data["addresses"][0]["address"]["freeformAddress"]
            else:
                address = None
        else:
            address = None

        results.append({"address": address, "status_code": status_code})

    #Creates and returns data frame
    return pd.DataFrame(results)

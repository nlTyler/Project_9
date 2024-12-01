import math
import time
import requests
import pandas as pd

def findCoordinates(address, key=None):
    """
        Finds latitude and longitude coordinates for a list of addresses using the TomTom API.

        Args:
            addresses (list): List of address strings.
            key (str): API key for the TomTom API. Defaults to global `api_key`.

        Returns:
            pd.DataFrame: DataFrame with columns ['lat', 'lng', 'address', 'status_code'].
        """
    if key is None:
        key = "gTGlKsrxmGjsdTE0TN71A8wSxAM4GbCl"
    base_url = 'https://api.tomtom.com/search/2/geocode/'


    results = []

    for addr in address:
        time.sleep(0.1)
        # Replace characters with hexadecimal equivalents
        addr = addr.replace(" ", "%20").replace(",", "%2C").replace("#", "%23")

        # Construct the query URL
        url = f'{base_url}{addr}.json'

        # Make the GET request
        response = requests.get(url, params={'key': key})

        # Record and return the response
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                lat = data['results'][0]['position']['lat']
                lng = data['results'][0]['position']['lon']
                address_found = data['results'][0]['address']['freeformAddress']
                results.append([lat, lng, address_found, response.status_code])
            else:
                results.append([math.nan, math.nan, addr, response.status_code])
        else:
            results.append([math.nan, math.nan, addr, response.status_code])

    # Create and return DataFrame
    return pd.DataFrame(results, columns=['lat', 'lng', 'address', 'status_code'])



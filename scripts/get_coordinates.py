import logging
from typing import Any
import requests

def get_coordinates(city: str, country: str = None) -> dict[str, Any] | None:
    """
    Returns the latitude and longitude coordinates for a specified city from the specified country.
    :param city: The city to get the coordinates for.
    :param country: The country in which the city is located.
    :return: { 'latitude': float, 'longitude': float, 'name': str, 'country': str } or None if not found
    """

    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        'name': city,
        'count': 1,
        'language': 'en',
        'format': 'json',
    }
    if country is not None: # In case country code hasn't been provided
        params['country'] = country

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            return {
                'latitude': result['latitude'],
                'longitude': result['longitude'],
                'name': result['name'],
                'country': result.get('country', 'Unknown'),  # To avoid error if no country provided
            }
        else:
            print(f"Coordinates not found for {city}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Network or API request error for {city}: {str(e)}")
    except Exception as e:
        logging.error(f"Error getting coordinates for {city}: {e}")
    return None

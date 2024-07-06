import requests
from requests.exceptions import HTTPError, Timeout
import re


def request_data():
    """
    Sends an HTTP GET request to the specified URL and returns the daily dates and cases.

    Returns:
        The scrapped data from the worlddometers site

    Raises:
        HTTPError: If an HTTP error occurs during the request.
        Timeout: If the request times out.
        Exception: If any other error occurs during the request.
    """
    try:
        response = requests.get("https://www.worldometers.info/coronavirus/country/south-africa/#graph-cases-daily", timeout=10, verify=False)
        response.raise_for_status()

        text = response.text
        datesMatch = match_iterate(text, "dates")
        with open('matches_dates.txt', 'w') as file:
            file.write(f"{datesMatch}\n")

        dataMatch = match_iterate(text, "data")
        with open('matches_data.txt', 'w') as file:
            file.write(f"{dataMatch}\n")
        
    except HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except Timeout as e:
        print(f"Request timed out: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return datesMatch, dataMatch 

def match_iterate(text, type ):
    pattern = re.compile(r'(\[((null,)|(\d{1,5},?))+\])') if type == "data" else re.compile(r'(\[("\w{3}\s\w{2},\s\d{4}",?)+\])')
    matches = pattern.finditer(text)
    # third index contains daily cases
    next(matches)
    next(matches)
    match = next(matches).group(1)
    return match
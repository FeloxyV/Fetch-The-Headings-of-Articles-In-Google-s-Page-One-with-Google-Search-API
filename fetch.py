import requests
from bs4 import BeautifulSoup
import pandas as pd


# Replace YOUR_API_KEY with your actual API key
API_KEY = "YOUR_API_KEY"

# Replace YOUR_CSE_ID with your actual CSE ID
CSE_ID = "YOUR_CSE_ID"

def search_google(query):
    """
    Make a search request to the Google Custom Search API
    """
    # Set up the search query parameters
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": 10
    }
    
    # Make the request
    try:
        resp = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
    except requests.exceptions.ConnectTimeout:
        print(f'Connection to Google Custom Search API timed out.')
        return []
    except requests.exceptions.ReadTimeout:
        print(f'Read timeout for Google Custom Search API.')
        return []
    
    # Check the response status code
    if resp.status_code != 200:
        print(f'An error occurred: {resp.status_code}')
        return []
    
    # Return the list of search results
    return resp.json()["items"]
    print(resp.text)

def parse_page_to_sections_list(link):
    """
    Simple function to download the raw html of a link
    parses contents into an array of dictionaries
    """
    # Set the connection and read timeout values
    timeout = (3.05, 27)
    
    # Download the page using the requests.get() function
    try:
        page = requests.get(link, timeout=timeout)
    except requests.exceptions.ConnectTimeout:
        print(f'Connection to {link} timed out.')
        return []
    except requests.exceptions.ReadTimeout:
        print(f'Read timeout for {link}.')
        return []
    
    # Parse the page contents using Beautiful Soup
    soup = BeautifulSoup(page.text, "lxml")

    title = soup.find("title").text

    headers = ['h1', 'h2', 'h3', 'h4', 'h5']

    df_json = []

    for header in headers:
        sections = soup.find_all(header)

        order = 0
        for section in sections:
            tmp = {
                "url": link,
                "page_title": title,
                "header": header,
                "order": order,
                "title": section.text
            }
            df_json.append(tmp)
            order = order + 1

    return df_json

# Set the search query
query = "how to box"

# Make a search request to Google
results = search_google(query)

# Create a list to store the parsed page data
df_master_list = []

# Loop over the search results
for result in results:
    # Get the link of the search result
    link = result["link"]
    
    # Check if the link is not an empty list
    if link:
        # Call the parse_page_to_sections_list() function to parse the page at the link
        df_json = parse_page_to_sections_list(link)
        
        # Append the data to the df_master_list list
        df_master_list.extend(df_json)

# Convert the df_master_list list to a Pandas DataFrame
df = pd.DataFrame(df_master_list)

# Save the DataFrame to a CSV file
df.to_csv("search_sections_for_{}.csv".format(query), index=False)

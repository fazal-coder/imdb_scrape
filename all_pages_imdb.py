import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

# Define the base URL for IMDb search
base_url = 'https://www.imdb.com/search/title/?count=100&groups=top_1000&sort=user_rating'

# Lists to store scraped data
movie_name = []
year = []
time = []
rating = []
metascore = []
votes = []
gross = []

# Define the pagination variables
current_page = 1
max_pages = 10  # 10

while current_page <= max_pages:
    # Build the URL for the current page
    url = f'{base_url}&start={(current_page - 1) * 100 + 1}'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    movie_data = soup.findAll('div', attrs={'class': 'lister-item mode-advanced'})

    for store in movie_data:
        name = store.h3.a.text
        year1 = store.h3.find('span', class_='lister-item-year').text
        dur = store.p.find('span', class_='runtime').text
        rating_div = store.find('div', class_='ratings-bar')
        imdb_rating = rating_div.find('strong').text

    # Extract the Metascore
        metascore_div = store.find('div', class_='inline-block ratings-metascore')
        if metascore_div:
            metascore_value = metascore_div.find('span', class_='metascore favorable')
            if metascore_value:
                metascore_value = metascore_value.text.strip()
            else:
                metascore_value = "N/A"
        else:
            metascore_value = "N/A"
            
        #Extract Votes
        votes_div = store.find('div', class_='lister-item-content')
        if votes_div:
            votes_number_element = votes_div.find('span', {'name': 'nv'})
            if votes_number_element:
                votes_number = votes_number_element['data-value']
                votes_number = votes_number.replace(',', '')  # Remove commas to get the numeric value
            else:
                votes_number = "N/A"
        else:
            votes_number = "N/A"

        #Extract Gross
        gross_span = store.select('span:-soup-contains("Gross:") + span[name="nv"]')

        if gross_span:
            gross_value = gross_span[0].text
        else:
            gross_value = "N/A"

        # Check if the value contains a '$' character before splitting
        if '$' in gross_value:
            gross_value = gross_value.split('$')[1]
        else:
            gross_value = "N/A"


        movie_name.append(name)
        year.append(year1)
        time.append(dur)
        rating.append(imdb_rating)
        metascore.append(metascore_value)
        votes.append(votes_number)
        gross.append(gross_value)

    current_page += 1


# Only Year
pattern = r'\d{4}'

# Extract 4-digit years from the strings
years = [int(re.search(pattern, s).group()) if re.search(pattern, s) else None for s in year]

# Filter out None values (unmatched patterns)
year_as_int = [y for y in years if y is not None]


# Create a DataFrame from the scraped data
data = {
    'Movie Name': movie_name,
    'Year': year_as_int,
    'Duration': time,
    'IMDb Rating': rating,
    'Metascore': metascore,
    'Votes': votes,
    'Gross': gross
}

df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv('imdb_movie_data.csv', index=False)

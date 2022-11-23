import requests
from bs4 import BeautifulSoup
import pandas as pd


domain = 'https://www.airbnb.co.in'
url = 'https://www.airbnb.co.in/s/Europe/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&place_id=ChIJhdqtz4aI7UYRefD8s-aZ73I&date_picker_type=calendar&checkin=2022-12-07&checkout=2022-12-11&adults=2&source=structured_search_input_header&search_type=filter_change'

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
next = soup.find('a',{'aria-label':'Next'}).get('href')
print(next)
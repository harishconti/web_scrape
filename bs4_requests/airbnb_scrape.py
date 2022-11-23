import requests
from bs4 import BeautifulSoup
import pandas as pd

domain = 'https://www.airbnb.co.in'
url = 'https://www.airbnb.co.in/s/Europe/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=5&place_id=ChIJhdqtz4aI7UYRefD8s-aZ73I&date_picker_type=calendar&checkin=2022-12-07&checkout=2022-12-11&adults=2&source=structured_search_input_header&search_type=filter_change'
url = 'https://www.airbnb.co.in/s/United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=3&date_picker_type=calendar&checkin=2022-12-15&checkout=2022-12-18&source=structured_search_input_header&search_type=unknown&adults=2&place_id=ChIJCzYy5IS16lQRQrfeQ5K5Oxw'
col = ['image_link','full_link','title','desc','beds','price','rating','num of ratings']
df_final = pd.DataFrame(columns = col)


def page_one(url):
  page = requests.get(url)
  soup = BeautifulSoup(page.text, 'lxml')
  next = soup.find('a',{'aria-label':'Next'}).get('href')
  return soup

def next_pages(domain, next):
  next_url = domain + next
  page = requests.get(next_url)
  soup = BeautifulSoup(page.text, 'lxml')
  return soup


def fetch(d_b):
  title = d_b.find('div', class_ = 't1jojoys dir dir-ltr').text
  desc = d_b.find('div', class_ ='nquyp1l s1cjsi4j dir dir-ltr').text
  beds = d_b.find('span', class_ =' dir dir-ltr').text
  price = d_b.find('span', class_ ='a8jt5op dir dir-ltr').text
  rating = d_b.find('span', class_ ='r1dxllyb dir dir-ltr').text
  rating, num_of_rev=rating.split(' ')
  full_link = domain + d_b.find('a', class_= 'bn2bl2p dir dir-ltr').get('href')
  img_link = d_b.find('div', class_ = '_1h6n1zu').find_all('source')[0].get('srcset')[:-3]
  arr = [img_link, full_link, title, desc, beds, price,rating, num_of_rev]
  return arr

def blocks(soup):
  blocks = soup.find_all('div', class_ = 'c1l1h97y dir dir-ltr')
  #print(len(blocks))
  df = pd.DataFrame(columns = col)
  for d_b in range(len(blocks)):
    try:
      #print(blocks[d_b])
      data = fetch(blocks[d_b])
      print(data)
      df.loc[d_b] = data

    except:
      pass
  return df

soup = page_one(url)
df = blocks(soup)
df_final = pd.concat([df_final,df])
while True:
  try:
    next = soup.find('a',{'aria-label':'Next'}).get('href')
    soup = next_pages(domain, next)
    #print(soup)
    df = blocks(soup)
    #print(df)
    df_final = pd.concat([df_final,df],ignore_index=True)
  except:
    break
print(df_final)
df_final.to_csv('airbnb_data.csv')
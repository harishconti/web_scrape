from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(r'chrome\chromedriver.exe', options=chrome_options)
driver.get('https://www.nike.com/in/w/mens-clothing-6ymx6znik1')

old_h = driver.execute_script('return document.body.scrollHeight')
while True:
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    time.sleep(5)
    new_h = driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    print(driver.execute_script('return document.body.scrollHeight'))
    time.sleep(5)
    if new_h == old_h:
        break
    old_h = new_h

soup = BeautifulSoup(driver.page_source, 'html5lib')
body = soup.find_all('div', class_=r'product-card__body')
arr = []
col = ['Product_title', 'sub_title', 'price', 'colors', 'product_link']
df = pd.DataFrame(columns=col)
for b in range(len(body)):
    title = body[b].find('div', class_='product-card__title').text
    sub_title = body[b].find('div', class_='product-card__subtitle').text
    price = body[b].find('div', class_='product-card__price').text
    colors = body[b].find('div', class_='product-card__count-item').text
    pro_link = body[b].find('a', class_='product-card__img-link-overlay').get('href')
    # print(title, sub_title, price, colors)
    arr = [title, sub_title, price, colors, pro_link]
    df.loc[b] = arr

# print(df)
df.to_csv('data/nike.csv')
link = df['product_link'][1]
driver.get(link)

driver.close()
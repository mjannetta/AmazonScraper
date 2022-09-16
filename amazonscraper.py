import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

records = []

def get_url(search):
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss_1'
    search = search.replace(' ', '+')
    url = template.format(search)
    url += '&page={}'
    return url

def get_item_info(item):
    atag = item.h2.a
    description = atag.text.strip()
    url = 'https://www.amazon.com' + atag.get('href')
    try:
        price_parent = item.find('span', 'a-price')
        price = price_parent.find('span', 'a-offscreen').text
    except AttributeError:
        price = 'Sold Out'
    item_info = (description, price, url)
    return item_info

def search_items(search_term):
    global records
    ser = Service(r"C:\Users\micha\Downloads\chromedriver_win32\chromedriver.exe")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)

    url = get_url(search_term)

    for page in range(1, 5):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = get_item_info(item)
            if record:
                records.append(record)
    driver.close()

def main():
    search_term = input("Enter the item you would like to scrape for: ")
    search_items(search_term)
    for i in records:
        print(i[1] + ' - ' + i[0] + ' - ' + i[2])
main()

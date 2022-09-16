from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from re import sub
from decimal import Decimal

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
    records = []
    ser = Service(r"C:\Users\micha\Downloads\chromedriver_win32\chromedriver.exe")
    op = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=op)

    url = get_url(search_term)

    for page in range(1, 2):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = get_item_info(item)
            if record:
                records.append(record)
    driver.close()
    return records


def print_results(results):
    for i in results:
        print(i[1] + ' - ' + i[0] + ' - ' + i[2])


def sort_results_price(results):
    length = len(results)
    for i in range(0, length):
        for j in range(0, length-i-1):
            if results[j][1] == 'Sold Out' or results[j+1][1] == 'Sold Out':
                if results[j][1] > results[j+1][1]:
                    temp = results[j]
                    results[j] = results[j+1]
                    results[j+1] = temp
            else:
                price_num_1 = Decimal(sub(r'[^\d.]', '', results[j][1]))
                price_num_2 = Decimal(sub(r'[^\d.]', '', results[j+1][1]))
                if price_num_1 > price_num_2:
                    temp = results[j]
                    results[j] = results[j + 1]
                    results[j + 1] = temp
    return results


def sort_results_alphabetically(results):
    length = len(results)
    for i in range(0, length):
        for j in range(0, length - i - 1):
            if results[j][0] > results[j + 1][0]:
                temp = results[j]
                results[j] = results[j + 1]
                results[j + 1] = temp
    return results


def main():
    search_term = input("Enter the item you would like to scrape for: ")
    search_results = search_items(search_term)
    search_results = sort_results_price(search_results)
    print_results(search_results)


main()

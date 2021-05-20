from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup

mf = "Invesco India Contra "


def browser_function(mf):
    options = webdriver.ChromeOptions()
    #options.add_argument('headless')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome("./config/chromedriver.exe", options = options)
    driver.maximize_window()
    driver.get("https://www.rupeevest.com/Mutual-Funds-India/2169")
    driver.implicitly_wait(10)
    portfolio_click = driver.find_element_by_id("OverviewPortfolio_a")
    portfolio_click.click()
    driver.implicitly_wait(10)
    time.sleep(5)
    page = driver.page_source
    print(page)
    '''
    table = driver.find_element_by_id("holding_table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        for num, col in enumerate(cols):
            print(num, col.value)
    driver.implicitly_wait(10)
    driver.close()
    time.sleep(30)
    '''
    return page

def scrape_browser(page):
    print("-------------------------")
    print(page)
    soup = BeautifulSoup(page, 'lxml')
    soup = soup.prettify()
    print(soup)
    col_list = ['equity', 'sector', 'holding']
    data = pd.DataFrame(columns=col_list)
    #table_selector = soup.find('table', {'id' : 'holdings_table'})
    table_selector = soup.find(id = 'holdings_table')
    print("found table = ", table_selector)
    if table_selector is not None:
        row_selectors = table_selector.find_all('tr', style = 'pointer-events: auto;')
        for row_selector in row_selectors:
            col_selector = row_selector.find_all('td', style = 'pointer-events: auto;')
            for col in col_selector:
                col.get_text()
                col = col.strip()
                print(col)
    return data


page = browser_function(mf)
data = scrape_browser(page)

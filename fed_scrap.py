# scraper that goes through a sample inmate list and saves matches on
# Federal BOP inmate locator website
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import re
import pandas as pd
import os
import numpy as np
import time

# start chrome webdriver
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path="chrome_driver/chromedriver.exe")
actionChains = ActionChains(driver)

# load sample inmate data
df=pd.read_excel('input/sample inmate data.xlsx')
df.reset_index(inplace=True)
df=df.rename({'index':'inmate_id'},axis=1)
# start dataframe to store inmate results
result_df=pd.DataFrame()

# find results for every inmate
for i,row in df.iterrows():
    print('scraping',row.First,row.Last)
    # go to the Federal inmate locator website
    driver.get('https://www.bop.gov/inmateloc/')
    time.sleep(2)
    # click find by name if it's the first row
    if i==0:
        driver.find_element_by_xpath('//*[@class="ui-state-default ui-corner-top"]').click()
    # enter first and last names in respective search fields
    driver.find_element_by_id('inmNameFirst').send_keys(row.First)
    driver.find_element_by_id('inmNameLast').send_keys(row.Last)
    # click search
    driver.find_element_by_id('searchNameButton').click()
    time.sleep(1)
    # find the results table in the resulting source code
    table_html=driver.find_element_by_id('nameResult').get_attribute('innerHTML')
    # use pandas to read the html table
    result=pd.read_html(table_html)[0]
    # add inmate and candidate reference id's
    result.reset_index(inplace=True)
    result=result.rename({'index':'cand_id'},axis=1)
    result['inmate_id']=row.inmate_id
    # append the table to the result_df
    result_df=result_df.append(result)

result_df.to_csv('output/candidate matches.csv')

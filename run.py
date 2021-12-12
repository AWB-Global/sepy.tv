import os
import pandas as pd
import numpy as np
import csv
import json
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from bot._bot_config import *

os.environ['PATH'] += r"G:/drivers/windows"

# URL params in bot._bot_config,py
url = f'https://www.{domain_name}.{tld}/{q}'
options = Options()
options.add_argument(r"--user-data-dir=C:\Users\username\AppData\Local\Google\Chrome\User Data")
options.add_argument(r"--profile-directory=Default")
options.add_argument(r"--disable-extensions"); 
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(5)
#driver.maximize_window()
post_list = []
raw = driver.find_element(By.CLASS_NAME, "js-card-list.tv-card-container__ideas")                                                
posts = raw.find_elements(By.CLASS_NAME, "tv-feed__item.tv-feed-layout__card-item.js-feed__item--inited")

for post in posts:

    date = post.find_element(By.CLASS_NAME, "tv-card-stats__time").text
    ticker = post.find_element(By.CLASS_NAME, ("tv-widget-idea__symbol-info")).find_element(By.TAG_NAME, "a").text
    timeframe = post.find_element(By.CLASS_NAME, ("tv-widget-idea__info-row")).find_element(By.CSS_SELECTOR, "span:nth-child(3)").text
    #bias = post.find_element(By.CLASS_NAME, ("tv-idea-label")).text     #<<<------ disable for all posts without bias!
    trader = post.find_element(By.CLASS_NAME, ("tv-card-user-info__name")).text
    profile_url = post.find_element(By.CLASS_NAME, "tv-card-user-info__main-wrap.js-userlink-popup").get_attribute('href')
    avatar_url = post.find_element(By.CLASS_NAME, "tv-user-avatar__image").get_attribute('src')
    likes = post.find_element(By.CLASS_NAME, ("tv-social-row__start")).text
    commentCount = post.find_element(By.CLASS_NAME, ("tv-social-row__end.tv-social-row__end--adjusted")).text
    title = post.find_element(By.CLASS_NAME, "tv-widget-idea__title-row").find_element(By.TAG_NAME, "a").text
    content = post.find_element(By.CLASS_NAME, "tv-widget-idea__description-row.tv-widget-idea__description-row--clamped.js-widget-idea__popup").text
    href = post.find_element(By.CLASS_NAME,('tv-widget-idea__cover-link.js-widget-idea__popup')).get_attribute('data-href')
    chart_img_url = post.find_element(By.CLASS_NAME, "tv-widget-idea__cover").get_attribute('data-src')
    idea_data = post.get_attribute('data-card')
    data_uid = post.get_attribute('data-uid')
    base_url = 'https://www.tradingview.com'
    
    post_item = {
        'Date':date,
        'Ticker': ticker,
        'Timeframe': timeframe,
        #'Bias':bias,
        'Trader': trader,
        'Profile_Url':profile_url,
        'Avatar_Url': avatar_url,
        'Likes':likes,
        'Comments':commentCount,
        'Title': title,
        'Content': content,
        'href': base_url + href, 
        'Chart_Img_Url': chart_img_url,
        'Idea_Data': idea_data,
        'Data_UID': data_uid,
        
    }       

    # saving the dataframe to a csv     
    post_list.append(post_item)
    df = pd.DataFrame(post_list)
    df.to_csv('out/tradingview-ideas.csv')
    print(df)

    # Serializing json 
    json_object = json.dumps(post_list, indent = 4)

    # Writing to .json
    with open("out/tradingview-ideas.json", "w") as outfile:
        outfile.write(json_object)

    # Writing to .txt
    filename = 'out/tradingview-ideas.txt'
    df.to_csv(filename, index = False, sep='|')

driver.close() # close session
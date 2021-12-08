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
#options = Options()
#options.add_argument(r"--user-data-dir=C:\Users\username\AppData\Local\Google\Chrome\User Data")
#options.add_argument(r"--profile-directory=Default")
#options.add_argument(r"--disable-extensions"); 
driver = webdriver.Chrome()
driver.get(url)
driver.implicitly_wait(5)
driver.maximize_window()
post_list = []
r=1
r2=2
post = driver.find_element_by_class_name('tv-content')                                                
while r < 4:
    try:
        json_data = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']').get_attribute('data-card')
        title = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']/div/div[1]/a[1]').text
        excerpt = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']/div/p').text
        img = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']/div/div[3]/span/picture/img').get_attribute('data-src')
        author = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']/div/div[4]/span[1]/a/span[2]/span').text
        ticker = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']/div/div[2]/div/a').text
        bias = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']/div/div[2]/span[3]').text
        href = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']/div/div[1]/a[1]').get_attribute('data-href')
        date = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r)+']/div/div[4]/span[3]/span/span').get_attribute('title')
        #likes = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/div['+str(r2)+']/div/div[5]/div[1]/span/span[3]').text
        #commentCount = post.find_element_by_xpath('.//*[@id="js-category-content"]/div/div/div/div/div/div[1]/div/div[1]/div['+str(r2)+']/div[2]/div/div[5]/div[2]/a/span[3]').text
        post_item = {
            'date':date,
            'author': author,
            'title': title,
            'excerpt': excerpt,
            'ticker': ticker,
            'bias':bias,
            #'likes':likes,
            #'commentcount':commentCount,
            'imgUrl': img,
            'href':url + href
        }       
        r +=1 # increment array index
        # saving the dataframe to a csv     
        post_list.append(post_item)
        df = pd.DataFrame(post_list)
        df.to_csv('out/tradingview.csv')
        print(df)
        # Serializing json 
        json_object = json.dumps(post_list, indent = 4)
  
        # Writing to .json
        with open("out/tradingview.json", "w") as outfile:
            outfile.write(json_object)

         # Writing to .txt
        filename = 'out/tradingview.txt'
        df.to_csv(filename, index = False, sep='|')

        # Number to txt with Numpy
        # numpy_array = df.to_numpy()
        # np.savetxt("test_file.txt", numpy_array, fmt = "%d")

    except NoSuchElementException: 
        break

driver.close() # close session
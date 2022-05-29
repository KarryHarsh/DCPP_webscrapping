
import os
from os import path
import pandas as pd
#from config.parameter import data_from,base_url,file_name,extension_url, online
#from utils import get_html,read_html
from selenium import webdriver
import codecs
import time
from selenium.webdriver.support.ui import WebDriverWait
base_url = "https://www.nasdaq.com"
def read_html(file_name):
    with open(file_name, "rb") as file:
        return file.read()

def get_html(base_url,file_name):
    #set chromedriver.exe path
    driver = webdriver.Chrome('driver/chromedriver.exe')
    driver.implicitly_wait(0.5)
    #maximize browser
    driver.maximize_window()
    #launch URL
    driver.get(base_url)
    time.sleep(5)
    # obtain page source
    h = driver.page_source
    #time.sleep(5)
    #open file in write mode with encoding
    f = codecs.open(file_name, "w", "utf−8")
    #write page source content to file
    f.write(h)
    #close browser
    driver.quit()

    return read_html(file_name)

data = pd.read_csv("data/csv/nasdaq_screener.csv")
data = data.sort_values(by=['Market Cap'], ascending=False).reset_index()

df = data[:100].copy()

#postfixes = ["dividend-history","news-headlines","pre-market","press-releases"
#             ,"after-hours", "financials","earnings"]
# for postfix in postfixes:
for i in range(len(df["Symbol"])):
    try:
        path1 = "data/html/company/" #+ df["Symbol"][i] + "/" + postfix
        os.makedirs(path1, exist_ok=True)
        url = base_url + "/market-activity/stocks/" + df["Symbol"][i].lower()# + "/" + postfix
        if not path.exists(path1 + df["Symbol"][i] + ".html"):
            data = get_html(url, path1 + df["Symbol"][i] + ".html")
            print("Directory {} created successfully".format(df["Symbol"][i] ))#+ "/" + postfix))

    except OSError as error:
        print("Directory '%s' can not be created")



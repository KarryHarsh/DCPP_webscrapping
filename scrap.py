import warnings
from bs4 import BeautifulSoup
from utils import get_html, read_html
import pandas as pd
from config.parameter import data_from, base_url, file_name, extension_url, online
import codecs
import time
import os
import requests

warnings.filterwarnings("ignore")

data = pd.read_csv("data/csv/nasdaq_screener.csv")
data = data.sort_values(by=['Market Cap'], ascending=False).reset_index()
df = data[:100].copy()

company_details_list = []
for i in range(len(df["Symbol"])):
    company_details = {}
    # data = get_html(base_url + extension_url + df["Symbol"][i]  , "data/html/company/" + df["Symbol"][i] +".html")
    data = read_html("data/html/company/" + df["Symbol"][i] + ".html")
    soup = BeautifulSoup(data, 'lxml')


    # stock_name_scrap = find_scrapper(soup,"address","company-profile__contact").find_all("a").
    def get_all_items(soup, tag1, class1, tag2, class2):
        # soup = BeautifulSoup(data, 'lxml')
        if class2:
            items = soup.find(tag1, class_=class1).find_all(tag2, cl ass_=class2)
        else:
            items = soup.find(tag1, class_=class1).find_all(tag2)
        return items


    address_html = get_all_items(soup, tag1="address", class1="company-profile__contact", tag2="a", class2=None)
    address = [add.text for add in address_html]
    company_details["company_address"] = address[0]
    # company_address.append({"company_address":  address[0]})
    # company_contact.append({"company_contact":  address[1]})
    # company_url.append({"company_url":  address[2]})
    company_details["company_contact"] = address[1]
    company_details["company_url"] = address[2]
    try:
        description1 = soup.find("span",
                                 class_="company-profile__description-excerpt company-profile__description-excerpt--ellipsis").text
        description2 = soup.find("span", class_="company-profile__description-remainder").text  # .find_all("a")
        description = description1 + description2
    except:
        description = " "
    # description_html = get_all_items(soup,tag1 = "div",class1 = "company-profile__description company-profile__description--expanded",tag2 = "span",class2 = None)

    company_details["company description"] = description

    key_executives_title = soup.find_all("td", class_="company-executives-title company-executives__table-cell")
    title_name = [title.text for title in key_executives_title]
    # executive_titles.append(({"executive_titles":title_name}))
    company_details["executive_titles"] = title_name

    key_executives_names = soup.find_all("th", class_="company-executives-name company-executives__table-cell")
    name = [name.text for name in key_executives_names]
    # executive_names.append({"executive_names":name})
    company_details["executive_names"] = name

    pricing = soup.find("span", class_="symbol-page-header__pricing-price").text
    company_details["stock price"] = pricing
    company_details["Symbol"] = df["Symbol"][i]
    company_details_list.append(company_details)
    print("Completed: {}".format(df["Symbol"][i]))
df1 = pd.DataFrame(company_details_list)

########################################################

company_realtime_details_list = []
for i in range(len(df["Symbol"])):
    company_details = {}
    try:
        path = "data/html/company/" + df["Symbol"][i] + "/real-time"
        os.makedirs(path, exist_ok=True)
        print("Directory {} created successfully".format(df["Symbol"][i] + "/real-time"))
    except OSError as error:
        print("Directory '%s' can not be created")
    data = read_html(path + df["Symbol"][i] + ".html")

    # data = get_html(base_url + extension_url + df["Symbol"][i]+"/real-time", path + df["Symbol"][i] + ".html")
    soup = BeautifulSoup(data, 'lxml')
    real_time_trade = soup.find_all("th", class_="real-time-trades-info__cell")
    real_time_trade_info = [info.text for info in real_time_trade]
    # executive_titles.append(({"executive_titles":title_name}))
    # company_details["executive_titles"] = title_name

    real_time_trade_value = soup.find_all("td", class_="real-time-trades-info__cell")
    real_time_trade_value_info = [value.text for value in real_time_trade_value]
    # executive_names.append({"executive_names":name})
    # company_details["executive_names"] = name

    company_details = {real_time_trade_info[i]: real_time_trade_value_info[i] for i in range(len(real_time_trade_info))}
    company_details["Symbol"] = df["Symbol"][i]
    company_realtime_details_list.append(company_details)

df2 = pd.DataFrame(company_realtime_details_list)

############################################################

company_realtime_details_list = []
for i in range(len(df["Symbol"])):
    company_details = {}
    try:
        path = "data/html/company/" + df["Symbol"][i] + "/after-hours"
        os.makedirs(path, exist_ok=True)
        print("Directory {} created successfully".format(df["Symbol"][i] + "/after-hours"))
    except OSError as error:
        print("Directory '%s' can not be created")
    data = read_html(path + df["Symbol"][i] + ".html")
    url = base_url + "/market-activity/stocks/" + df["Symbol"][i].lower() + "/after-hours"
    # data = get_html(url, path + df["Symbol"][i] + ".html")
    soup = BeautifulSoup(data, 'lxml')
    real_time_trade = soup.find_all("th", class_="after-hours-quote-info__cell")
    real_time_trade_info = [info.text for info in real_time_trade]
    # executive_titles.append(({"executive_titles":title_name}))
    # company_details["executive_titles"] = title_name

    real_time_trade_value = soup.find_all("td", class_="after-hours-quote-info__cell")
    real_time_trade_value_info = [value.text for value in real_time_trade_value]
    # executive_names.append({"executive_names":name})
    # company_details["executive_names"] = name

    company_details = {real_time_trade_info[i]: real_time_trade_value_info[i] for i in range(len(real_time_trade_info))}
    company_details["Symbol"] = df["Symbol"][i]
    company_realtime_details_list.append(company_details)

df3 = pd.DataFrame(company_realtime_details_list)

###########################################################


company_realtime_details_list = []
for i in range(len(df["Symbol"])):
    company_details = {}
    try:
        path = "data/html/company/" + df["Symbol"][i] + "/pre-market"
        os.makedirs(path, exist_ok=True)
        print("Directory {} created successfully".format(df["Symbol"][i] + "/pre-market"))
    except OSError as error:
        print("Directory '%s' can not be created")
    data = read_html(path + df["Symbol"][i] + ".html")
    url = base_url + "/market-activity/stocks/" + df["Symbol"][i].lower() + "/pre-market"
    # data = get_html(url, path + df["Symbol"][i] + ".html")
    soup = BeautifulSoup(data, 'lxml')
    real_time_trade = soup.find_all("th", class_="pre-market-quote-info__cell")
    real_time_trade_info = [info.text for info in real_time_trade]
    # executive_titles.append(({"executive_titles":title_name}))
    # company_details["executive_titles"] = title_name

    real_time_trade_value = soup.find_all("td", class_="pre-market-quote-info__cell")
    real_time_trade_value_info = [value.text for value in real_time_trade_value]
    # executive_names.append({"executive_names":name})
    # company_details["executive_names"] = name

    company_details = {real_time_trade_info[i]: real_time_trade_value_info[i] for i in range(len(real_time_trade_info))}
    company_details["Symbol"] = df["Symbol"][i]
    company_realtime_details_list.append(company_details)

df4 = pd.DataFrame(company_realtime_details_list)

##############################################

list_hrefs = []
list = []
for i in range(len(df["Symbol"])):
    company_details = {}
    try:
        path = "data/html/company/" + df["Symbol"][i] + "/news-headlines"
        os.makedirs(path, exist_ok=True)
        print("Directory {} created successfully".format(df["Symbol"][i] + "/news-headlines"))
    except OSError as error:
        print("Directory '%s' can not be created")
    data = read_html(path + df["Symbol"][i] + ".html")
    url = base_url + "/market-activity/stocks/" + df["Symbol"][i].lower() + "/news-headlines"
    # data = get_html(url, path + df["Symbol"][i] + ".html")
    soup = BeautifulSoup(data, 'lxml')
    try:
        company_details["Symbol"] = df["Symbol"][i]
        head_lines = soup.find_all("p", class_="quote-news-headlines__item-title")
        head_lines_info = [head_line.text for head_line in head_lines]
        company_details["news_headlines"] = head_lines_info
        links = soup.find_all("li", class_="quote-news-headlines__item")
        for link in links:
            href = link.find("a")
            list_hrefs.append(base_url + href['href'])
        company_details["news_headlines_links"] = list_hrefs
    except:
        company_details["news_headlines"] = ""
        company_details["news_headlines_links"] = ""

    list.append(company_details)

df5 = pd.DataFrame(list)

##########################################################

list_hrefs = []
list = []
for i in range(len(df["Symbol"])):
    company_details = {}
    try:
        path = "data/html/company/" + df["Symbol"][i] + "/press-releases"
        os.makedirs(path, exist_ok=True)
        print("Directory {} created successfully".format(df["Symbol"][i] + "/press-releases"))
    except OSError as error:
        print("Directory '%s' can not be created")
    data = read_html(path + df["Symbol"][i] + ".html")
    url = base_url + "/market-activity/stocks/" + df["Symbol"][i].lower() + "/press-releases"
    # data = get_html(url, path + df["Symbol"][i] + ".html")
    soup = BeautifulSoup(data, 'lxml')
    # head_lines = soup.find_all("h3", class_="quote-press-release__card-title")
    # head_lines_info = [head_line.text for head_line in head_lines]
    # company_details["news_headlines"] = head_lines_info
    links = soup.find_all("h3", class_="quote-press-release__card-title")
    head_lines_info = [link.text for link in links]
    company_details["pre_releases_header"] = head_lines_info
    for link in links:
        href = link.find("a")
        list_hrefs.append(base_url + href['href'])
    company_details["pre_releases_links"] = list_hrefs
    company_details["Symbol"] = df["Symbol"][i]

    list.append(company_details)

df6 = pd.DataFrame(list)

##########################################################

list = []
for i in range(len(df["Symbol"])):
    company_details = {}
    try:
        path = "data/html/company/" + df["Symbol"][i] + "/dividend-history"
        os.makedirs(path, exist_ok=True)
        print("Directory {} created successfully".format(df["Symbol"][i] + "/dividend-history"))
    except OSError as error:
        print("Directory '%s' can not be created")
    data = read_html(path + df["Symbol"][i] + ".html")
    url = base_url + "/market-activity/stocks/" + df["Symbol"][i].lower() + "/dividend-history"
    # data = get_html(url, path + df["Symbol"][i] + ".html")
    soup = BeautifulSoup(data, 'lxml')
    dividend_history_keys = soup.find_all("span", class_="dividend-history__summary-item__label")
    dividend_history_keys_info = [dividend_history_key.text for dividend_history_key in dividend_history_keys]
    # executive_titles.append(({"executive_titles":title_name}))
    # company_details["executive_titles"] = title_name

    dividend_history_values = soup.find_all("span", class_="dividend-history__summary-item__value")
    dividend_history_value_info = [dividend_history_value.text for dividend_history_value in dividend_history_values]
    # executive_names.append({"executive_names":name})
    # company_details["executive_names"] = name

    company_details = {dividend_history_keys_info[i]: dividend_history_value_info[i] for i in
                       range(len(dividend_history_keys_info))}
    company_details["Symbol"] = df["Symbol"][i]
    list.append(company_details)
df7 = pd.DataFrame(list)

list = []

for i in range(len(df["Symbol"])):
    company_details = {}
    company_details["Symbol"] = df["Symbol"][i]
    try:
        path = "data/html/company/" + df["Symbol"][i] + "/financials"
        os.makedirs(path, exist_ok=True)
        print("Directory {} created successfully".format(df["Symbol"][i] + "/financials"))
    except OSError as error:
        print("Directory '%s' can not be created")
    data = read_html(path + df["Symbol"][i] + ".html")
    url = base_url + "/market-activity/stocks/" + df["Symbol"][i].lower() + "/financials"
    # data = get_html(url, path + df["Symbol"][i] + ".html")
    soup = BeautifulSoup(data, 'lxml')
    table1 = soup.find_all("div", class_="financials__panel")
    inc = 1
    for tab in table1:

        for table in tab.find_all("table"):
            # print(table.text)
            headers = []
            for i in table.find_all("th"):
                title = i.text
                headers.append(title)
            cols = headers[1:5]
            rows = headers[5:]
            data = []
            for j in table.find_all("tr")[1:]:
                row_data = j.find_all("td")
                row = [i.text for i in row_data]
                data.append(row)
            dfx = pd.DataFrame(data, rows, cols)
            # converting to dict
            data_dict = dfx.to_dict()
            company_details["financials" + str(inc)] = data_dict
            inc = inc + 1

    # company_details["company_code"] = df["Symbol"][i]
    list.append(company_details)

df8 = pd.DataFrame(list)

import functools as ft

dfs = [df, df1, df2, df3, df4, df5, df6, df7, df8]
df_final = ft.reduce(lambda left, right: pd.merge(left, right, on='Symbol'), dfs)

df_final.to_csv("data/csv/Harsh_scrapped_df.csv", index=False, header=True, encoding="utf-8")
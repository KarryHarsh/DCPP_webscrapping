#!/usr/bin/env python
# coding: utf-8

# In[29]:


import pandas as pd
import warnings
import numpy as np
warnings.filterwarnings("ignore")

pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 70)


# In[30]:


df = pd.read_csv("data/csv/Harsh_scrapped_df.csv")
df.head()


# In[31]:


df.shape


# ### Inconsidtence Column Name
# 
# * Change Case
# * Rename Them

# In[32]:


df["Symbol"]


# In[33]:


# Upper casing the Column Names
df.columns = df.columns.str.upper()
df.columns


# In[34]:


df.rename(columns = {"% CHANGE":"PERCENTAGE CHANGE",
                     "NASDAQ LAST SALE (NLS) PLUS VOLUME":"NLS VOLUME",
                     "_X":"AFTER STOCK DIRECTION",
                    "_Y":"PRE STOCK DIRECTION",
                    "FINANCIALS1":"INCOME STATEMENT",
                    "FINANCIALS2":"BALANCE SHEET",
                    "FINANCIALS3":"CASH FLOW",
                    "FINANCIALS4":"FINANCIAL RATIO",
                    "UNNAMED: 27":"STOCK TREND"}, inplace = True)

df.columns


# ### MISSING DATA

# In[35]:


df.isnull().sum()/df.shape[0] *100


# In[36]:


# null values coumns
df.isnull().sum().sum()


# In[37]:


df = df.fillna(0)


# In[38]:


df.drop("INDEX", axis=1, inplace=True)


# In[39]:


g = df.columns.to_series().groupby(df.dtypes).groups
g


# In[40]:


df.head()


# In[41]:


df['IPO YEAR'] = df["IPO YEAR"].astype(np.int64)

# Convert each value of the column to a string
#df['NLS VOLUME'] = pd.to_numeric(df['NLS VOLUME'])
#df['PRE-MARKET VOLUME'] = pd.to_numeric(df['PRE-MARKET VOLUME'])

#df['EX-DIVIDEND DATE'] =  pd.to_datetime(df['EX-DIVIDEND DATE'], format='%b/%d/%Y')


# In[42]:


df[["TODAY'S HIGH","TODAY'S LOW"]] = df["TODAY'S HIGH / LOW"].str.split('/',expand=True)
df[["52 WEEK HIGH","TODAY'S LOW"]] = df["52 WEEK HIGH / LOW"].str.split('/',expand=True)
df[["AFTER CLS","AFTER CLS MARGIN","AFTER CLS PERCENTAGE"]] = df["CONSOLIDATED LAST SALE"].str.split(' ',expand=True)
#df[["BEFORE CLS","BEFORE CLS MARGIN","BEFORE CLS PERCENTAGE"]] = df["CONSOLIDATED LAST SALE_Y"].str.split(' ',expand=True)


# In[43]:


#first_word = re.split("\s", my_string)[0]
#df[["AFTER-HOURS HIGH($)"]] = df["AFTER-HOURS HIGH"].str.split(' ',1)
df['AFTER-HOURS HIGH'] = df['AFTER-HOURS HIGH'].str.split(' ').str[0]
df['AFTER-HOURS LOW'] = df['AFTER-HOURS LOW'].str.split(' ').str[0]

#df['PRE-MARKET HIGH'] = df['PRE-MARKET HIGH'].str.split(' ').str[0]
#df['PRE-MARKET LOW'] = df['PRE-MARKET LOW'].str.split(' ').str[0]


# In[44]:


columns = ["LAST SALE","STOCK PRICE", "PREVIOUS CLOSE","TODAY'S HIGH","TODAY'S LOW","52 WEEK HIGH"
          ,"AFTER-HOURS HIGH","AFTER-HOURS LOW"]

for col in columns:
    df[col] = df[col].str.split('$').str[1]
    df[col] = pd.to_numeric(df[col])
    print(col)


# In[45]:


columns = ["LAST SALE","STOCK PRICE", "PREVIOUS CLOSE","TODAY'S HIGH","TODAY'S LOW","52 WEEK HIGH"
          ,"AFTER-HOURS HIGH","AFTER-HOURS LOW","ANNUAL DIVIDEND"]

for col in columns:
    df.rename(columns = {col :col+ "($)"
                    }, inplace = True)

df.columns


# In[46]:


column = ['SYMBOL', 'NAME', 'LAST SALE($)', 'NET CHANGE', 'PERCENTAGE CHANGE',
       'MARKET CAP', 'COUNTRY', 'IPO YEAR', 'VOLUME', 'SECTOR', 'INDUSTRY',
       'COMPANY_ADDRESS', 'COMPANY_CONTACT', 'COMPANY_URL',
       'COMPANY DESCRIPTION', 'EXECUTIVE_TITLES', 'EXECUTIVE_NAMES',
       'STOCK PRICE($)', 'NLS VOLUME', 'PREVIOUS CLOSE($)',
       'TODAY'S HIGH / LOW', '52 WEEK HIGH / LOW', 'CONSOLIDATED LAST SALE',
       'AFTER-HOURS VOLUME', 'AFTER-HOURS HIGH($)', 'AFTER-HOURS LOW($)',
       'STOCK TREND', 'NEWS_HEADLINES', 'NEWS_HEADLINES_LINKS',
       'PRE_RELEASES_HEADER', 'PRE_RELEASES_LINKS', 'EX-DIVIDEND DATE',
       'DIVIDEND YIELD', 'ANNUAL DIVIDEND($)', 'P/E RATIO', 'INCOME STATEMENT',
       'BALANCE SHEET', 'CASH FLOW', 'FINANCIAL RATIO', 'TODAY'S HIGH($)',
       'TODAY'S LOW($)', '52 WEEK HIGH($)', 'AFTER CLS', 'AFTER CLS MARGIN',
       'AFTER CLS PERCENTAGE']


# In[47]:


df.head()


# In[48]:


df.shape


# In[49]:


columns = ["TODAY'S HIGH / LOW"]

for col in columns:
    df.drop(col, axis=1, inplace=True)


# In[50]:


df.head()


# In[51]:


columns = ['SYMBOL', 'NAME', 'PERCENTAGE CHANGE', 'COUNTRY', 'SECTOR', 'INDUSTRY', 'COMPANY_ADDRESS', 'COMPANY_CONTACT', 'COMPANY_URL', 'COMPANY DESCRIPTION', 'EXECUTIVE_TITLES', 'EXECUTIVE_NAMES', 'NLS VOLUME', '52 WEEK HIGH / LOW', 'CONSOLIDATED LAST SALE', 'AFTER-HOURS VOLUME', 'STOCK TREND', 'NEWS_HEADLINES', 'NEWS_HEADLINES_LINKS', 'PRE_RELEASES_HEADER', 'PRE_RELEASES_LINKS', 'EX-DIVIDEND DATE', 'DIVIDEND YIELD', 'ANNUAL DIVIDEND($)', 'P/E RATIO', 'INCOME STATEMENT', 'BALANCE SHEET', 'CASH FLOW', 'FINANCIAL RATIO', 'AFTER CLS', 'AFTER CLS MARGIN', 'AFTER CLS PERCENTAGE']

for col in columns:
    df[col]= df[col].astype('str') 


# In[52]:


df.to_excel("NASDAQ_dataset.xlsx", index=False,header=True,encoding ="utf-8")


# In[53]:


data = df.to_json()


# In[28]:


import json
with open('nasdqa_data.json', 'w') as f:
    json.dump(data, f)


# In[24]:





# In[25]:


column = ['SYMBOL', 'NAME', 'LAST SALE($)', 'NET CHANGE', 'PERCENTAGE CHANGE',
       'MARKET CAP', 'COUNTRY', 'IPO YEAR', 'VOLUME', 'SECTOR', 'INDUSTRY',
       'COMPANY_ADDRESS', 'COMPANY_CONTACT', 'COMPANY_URL',
       'COMPANY DESCRIPTION', 'EXECUTIVE_TITLES', 'EXECUTIVE_NAMES',
       'STOCK PRICE($)', 'NLS VOLUME', 'PREVIOUS CLOSE($)',
       '52 WEEK HIGH / LOW', 'CONSOLIDATED LAST SALE', 'AFTER-HOURS VOLUME',
       'AFTER-HOURS HIGH($)', 'AFTER-HOURS LOW($)', 'STOCK TREND',
        'PRE_RELEASES_HEADER',
       'EX-DIVIDEND DATE', 'DIVIDEND YIELD',
       'ANNUAL DIVIDEND($)', 'P/E RATIO', "TODAY'S HIGH($)", "TODAY'S LOW($)",
       '52 WEEK HIGH($)', 'AFTER CLS', 'AFTER CLS MARGIN',
       'AFTER CLS PERCENTAGE']


# In[118]:


import sweetviz as sv
report = sv.analyze(df[column])
report.show_html("analyze.html")


# In[ ]:





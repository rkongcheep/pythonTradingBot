import numpy as np
import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import tqdm
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = Chrome('./chromedriver')
driver.maximize_window()

def go_to_company_page(company_symbol='ADVANC'):
    url = f'https://www.set.or.th/th/market/product/stock/quote/{company_symbol}/company-profile/major-shareholders'
    driver.get(url)
    WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.XPATH, f'//div[@class="col-12 col-md-6 mb-3 mb-md-0 d-none d-md-block"]')))

'''
Now for specific stock, we will pull
1. Total Sharenum
2. Price
3.0 Data Date
3. %Free Float
4. Num Free Float
5. Major Share Holder
    5.1 Name 
    5.2 Num Share Held
'''


def get_data(symbol='ADVANC'):
    go_to_company_page(symbol)
    price = (driver.find_element(By.XPATH,f'//h1[@class="value text-white mb-0 me-2 lh-1"]').text)
    if price != '-':
        price = float(price)
    as_date = (driver.find_element(By.XPATH,f'//div[@class="col-12 col-md-6 mb-3 mb-md-0 d-none d-md-block"]').text)
    free_float = (driver.find_elements(By.XPATH,f'//div[@class="col-12 col-md-6 mb-3 mb-md-0 d-flex flex-column"]/span')[1].text)
    if free_float != '-':
        free_float = float(driver.find_elements(By.XPATH,f'//div[@class="col-12 col-md-6 mb-3 mb-md-0 d-flex flex-column"]/span')[1].text)

    name = []
    share_quant = []
    share_quant_per = []

    for idx in range(10):
        try:
            name.append(driver.find_element(By.XPATH,f'//tr[@indexselected="{idx}"]/td[@aria-colindex="2"]').text)
            share_quant.append(float(driver.find_element(By.XPATH,f'//tr[@indexselected="{idx}"]/td[@aria-colindex="3"]').text.replace(',','')))
            share_quant_per.append(float(driver.find_element(By.XPATH,f'//tr[@indexselected="{idx}"]/td[@aria-colindex="4"]').text))
        except:
            break
        
    table = pd.DataFrame({'Name':name,'Quantity':share_quant,'Percent':share_quant_per,'Symbol':symbol,'AsOf':as_date,'Freefloat':free_float})
    # print(f'{price=}')
    # print(f'{as_date=}')
    # print(f'{free_float=}')
    # print(f'{table}')
    return table

# get_data('3K-BAT')

# price,as_date,free_float,table = get_data()
stock_list = pd.read_csv('StockNameIndust.csv')
# ss_ = stock_list.iloc[:450,:].copy()
# table = None
# i=1
# for symbol_i in (ss_.symbol):
#     print(symbol_i+' starting')
#     print(f'{i}/898')
#     try: 
#         table_ = get_data(symbol_i)
#     except:
#         print(f'break at {i=}')
#         break
#     if table is None:
#         table = table_.copy()
#     else:
#         table = pd.concat([table,table_])
#     i+=1

# table.to_csv('ALL1.csv',encoding='utf-8-sig')

# driver.quit()


# driver = Chrome('./chromedriver')
# driver.maximize_window()
i=450
table = None
ss_2 = stock_list.iloc[450:,:].copy()
for symbol_i in (ss_2.symbol):
    print(symbol_i+' starting2')
    print(f'{i}/898')
    try: 
        table_ = get_data(symbol_i)
    except:
        print(f'break at {i=}')
        break
    print(table_.head(1))
    if table is None:
        table = table_.copy()
    else:
        table = pd.concat([table,table_])
    i+=1

table.to_csv('ALL2.csv',encoding='utf-8-sig')





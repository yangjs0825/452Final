# import modules
import urllib.request  as urllib2
import re
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import string
from decimal import Decimal

def uniq():
    print('Please pick up the category you want')
    print('1. men, 2. women')
    choice = input('Please enter 1 or 2 to choose ')
    if choice == '1':
        content = urllib2.urlopen('https://www.uniqlo.com/us/en/men/sale').read()
    elif choice == '2':
        content = urllib2.urlopen('https://www.uniqlo.com/us/en/women/sale').read()
    else:
        print('Not a valid choice')
    # get the information from one of my favorite

    soup = BeautifulSoup(content,'lxml')

    # get all the sale items from website
    items = soup.find_all("div", class_='product-tile-info')
    # print(len(items))

    # collect and classify the information i need
    items_list = []
    prices = []
    old_prices = []
    saves = []
    save_pers = []
    for item1 in items:
        # get the list of items' name
        item = item1.find('img').get('alt')
        items_list.append(item)

        # get the current price
        price = item1.find('span', class_='product-sales-price').text
        prices.append(price)

        # get the original prices
        old_price = item1.find('span', class_='product-standard-price').text
        old_prices.append(old_price)

        # calculate saving money for each item
        save = float(old_price[1:]) - float(price[1:])
        saves.append(round(save,2))

        # calculate save percentage
        save_per = round(save/float(old_price[1:])*100,2)
        save_pers.append(save_per)

    # print(items_list)
    # print(prices)
    # print(old_prices)
    # print(saves)
    # print(save_pers)

    df = pd.DataFrame()
    df['items'] = items_list
    df['price'] = prices
    df['original price'] = old_prices
    df['saves'] = saves
    df['save_pers(%)'] = save_pers
    print(df)

# website work https://slickdeals.net/

def sd():
    content = urllib2.urlopen('https://slickdeals.net/').read()
    soup = BeautifulSoup(content,'lxml')

    # after review the page source, the information I need all in the tag 'div' with the class value equals 'fpGridBox grid frontpage cat'
    # soup.find_all will return a list with the elements.
    items = soup.find_all("div", class_='fpGridBox grid frontpage cat')
    # print(type(items))
    # print(len(items))
    # print(items)
    # print(content)

    # get the items title information
    titles = []
    symbols = ['&colon;', '&dollar;', '&comma;', '&percnt;', '&semi;', '&sol;', '&period;',
               '&plus;', '&amp;', '&lpar;', '&rpar;']
    # the symbols are :, $, , , %, ;, /, ", +
    relist = [':','$',',','%',';','/','"','+','&','(',')']
    prices = []
    old_prices = []
    stores = []
    for i in range(1,len(items)):
        title = items[i].find('img').get('title')
        # print(type(title))
        title = title.split('$')[0].lstrip()
        for x in range(11):
            if symbols[x] in title:
                title = title.replace(symbols[x],relist[x])
        titles.append(title)

        # get the items' price information
        price = items[i].find('div', class_='itemPrice').text
        price = price.split()[0]
        prices.append(price)

        # get the items' old price information
        old_price = items[i].find('span', class_='oldListPrice')
        # print(type(old_price))
        if old_price is None:
            old_prices.append(old_price)
        else:
            old_price = items[i].find('span', class_='oldListPrice').text
            old_prices.append(old_price)

        # # get the store information
        store = items[i].find('a', class_='itemStore')
        # store.replace('&nbsp;','')
        if store is None:
            stores.append(store)
        else:
            store = items[i].find('a', class_='itemStore').text
            store = store[:-1]
            stores.append(store)

    # print(titles)
    # print(prices)
    # print(old_prices)
    # print(stores)

    df = pd.DataFrame()
    df['items'] = titles
    df['price'] = prices
    df['original price'] = old_prices
    df['store'] = stores

    # print out the result
    print(df)

print('This is a program to get deals information.')
print('Please choose the website you are interested below:')
print('1. UNIQLO, 2. Slickdeals')
choice = input('Enter 1 or 2 to choose ')

if choice == '1':
    uniq()
elif choice == '2':
    sd()
else:
    print('Not a valid choice')

'''
Created on May 20, 2021
Houston, Harris County, Texas, United States
@author: Steven Shan
'''

from numpy import *
import pandas as pd
import datetime as dt
import json
import requests
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tkr

# To Do
# 1. Add a map to the country by origin
# 2. Now add item by country and time
# 3. Try all permutations of country/time/product
#To Add
#1. Drop Down Menus for Countries and Products
#2. GIS
#3. Make it more flexible (time) - type in a start/end year/month and then graph
#4. Interactive: Click and Get Info

def year_imports():
    # Import Gang  
# Total value by year
# Preparing the Various Values
# Only useful from 2013 - 2021
    year = input("Enter your desired year: ")
    URL_base = "https://api.census.gov/data/timeseries/intltrade/imports/hs?get=CON_CIF_YR&time="
    api_key = 'a71878ff361ea483f0788b1fe0687beeed9a2c1c'
    time_end = str(year);
    url = URL_base + time_end
    import_val_fetch = requests.get(url)
    cum_month_val = [0] * 12;
    ind_month_val = [0] * 12;
    count = 1;
    for element in cum_month_val:
        print(len(import_val_fetch.json()))
        if(len(import_val_fetch.json()) < (count + 1)):
            break;
        cum_month_val[count - 1] = (int) (import_val_fetch.json()[count][0]) / 1000000000
        count = count + 1
    ind_month_val[0] = cum_month_val[0]
    for x in range(1, 12):
        ind_month_val[x] = cum_month_val[x] - cum_month_val[x - 1]
        if(ind_month_val[x] < 0):
            ind_month_val[x] = 0
            break
        
    # This will be used to plot the values
    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    title_shell = "US imports in " + time_end + " - Cumulative by Month"
    plt.plot(months, ind_month_val, marker='X')
    plt.xticks(np.arange(min(months), max(months) + 1, 1.0))  # This is to print out all month values
    plt.title(title_shell)
    plt.ylabel("Imports (CIF) in billions")
    plt.xlabel("Month")
    print(title_shell)  #Print Table Then Show Graph
    print("month ", "Imports in billions")
    for x in range(0, 11):
        print(months[x], "    ", ind_month_val[x])
    plt.show()



def country_imports(countrycode):
#Imports by Country and Month
#Country Codes For Reference
# Mexico: 2010
# Canada: 1220
    year = input("Enter your desired year: ")
    country_code = str(countrycode)
    country_name = ""
    months = ['01', '02', '03', '04', '05','06', '07', '08', '09', '10', '11', '12']
    import_values = [None] * 12
    cumulative_import_values = [None] * 12
    count = 0;
    URL_base = 'https://api.census.gov/data/timeseries/intltrade/exports/hs?get=CTY_CODE,CTY_NAME,ALL_VAL_MO,ALL_VAL_YR&'
    for element in import_values:
        date_format = year + "-" + months[count];
        time_base = 'time=' + date_format
        country_base = '&CTY_CODE=' + country_code
        URL_fetch = URL_base + time_base + country_base  
        print(URL_fetch)
        import_val_fetch = requests.get(URL_fetch)
        country_name = import_val_fetch.json()[1][1] 
        import_val_fetch = requests.get(URL_fetch)
        import_values[count] = (int) (import_val_fetch.json()[1][2]) / 1000000000;
        if(count == 0):
            cumulative_import_values[0] = import_values[0]
            count = count + 1
        else:
            cumulative_import_values[count] = cumulative_import_values[count - 1] + import_values[count]
            count = count + 1

    months_yr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    title_shell = "US imports from " + country_name + " in " + year +  "- Cumulative and Individual by Month"
    plt.plot(months_yr, import_values, marker='X')
    plt.xticks(np.arange(min(months_yr), max(months_yr) + 1, 1.0))  # This is to print out all month values
    plt.title(title_shell)
    plt.ylabel("Imports (CIF) in billions")
    plt.xlabel("Month")
    print(title_shell)  #Print Table Then Show Graph
    print("month ", "Individual Imports", "Cumulative, Imports in ($)bn")
    for x in range(0, 12):
        print(months_yr[x], "    ", import_values[x], "    ", cumulative_import_values[x])
    plt.show()

# display amount and country
# monthly imports are easy to get
# imports by country
def product_imports():
    year = input("Enter your desired year: ")
    hs_commodity_code = input("Enter your desired HS commodity code: ")
    
    base_URL = 'https://api.census.gov/data/timeseries/intltrade/imports/hs?get=I_COMMODITY,I_COMMODITY_LDESC,GEN_VAL_MO'
    
    monthly_import_values = 12 * [0]
    months = ['01', '02', '03', '04', '05','06', '07', '08', '09', '10', '11', '12']
    import_monthly_val = [0] * 12
    commodity_description = ''
    
    count = 0
    for element in monthly_import_values:
        time_date_URL = '&time=' + year + "-" + months[count];
        commodity_code_URL = '&I_COMMODITY=' + hs_commodity_code
        URL_fetch = base_URL + time_date_URL + commodity_code_URL  
        import_val_fetch = requests.get(URL_fetch)
        try:
            import_monthly_val[count] = (int) (import_val_fetch.json()[1][2])/1000000 
        except Exception:
            print("Sorry, that trade data does not exist")
            break
        commodity_description = (import_val_fetch.json()[1][1])
        count = count + 1
    
    months_yr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    title_shell = "US imports of " + commodity_description + " in " + year + ": by month"
    plt.plot(months_yr, import_monthly_val, marker='X')
    plt.xticks(np.arange(min(months_yr), max(months_yr) + 1, 1.0))  # This is to print out all month values
    plt.title(title_shell)
    plt.ylabel("Imports (CIF) in millions")
    plt.xlabel("Month")
    print(title_shell)  #Print Table Then Show Graph
    print("month ", "Individual Imports", "Cumulative, Imports in ($)bn")
    for x in range(0, 12):
        print(months_yr[x], "    ", import_monthly_val[x])
    plt.show()

# For Now, Only Applies to Years
# Though Later, I will need to make it
# apply for months 
def product_import_all_country():
    # Setting Up The URL and various procedural things including creating the JSON
    year = input("Enter your desired year: ")
    hs_commodity_code = input("Enter your desired HS commodity code: ")
    url_base = 'https://api.census.gov/data/timeseries/intltrade/imports/hs?get=I_COMMODITY,I_COMMODITY_LDESC,CON_VAL_YR,CTY_CODE,CTY_NAME'
    time_string  = '&time=' + year + "-12"
    commodity_string = '&I_COMMODITY=' + hs_commodity_code 
    URL_probe = url_base + time_string + commodity_string
    import_val_fetch = requests.get(URL_probe)
    count = 0;
    potential_length = len(import_val_fetch.json())
    actual_length = 0;
    non_countries = 0;
    non_areas = 0;
    
    # This is used to count the number of countries and to populate that array
    commodity_item = "";
    for x in range(2, potential_length):
        if((import_val_fetch.json()[x][3].isdigit()) == False):
            non_countries = non_countries + 1
            continue
        elif ((int) (import_val_fetch.json()[x][3]) < 1000):
            non_areas = non_areas + 1
            continue
        commodity_item = import_val_fetch.json()[x][1]
        actual_length = actual_length + 1
    countries = [0] * actual_length 
    values = [0] * actual_length 
    
    # The number of spaces is (start - finish) + 2
    # This is used to scrap the JSON file and put it inot one
    for x in range(0, actual_length + 2):
        if((import_val_fetch.json()[x][3].isdigit()) == False):
            continue
        elif ((int) (import_val_fetch.json()[x][3]) < 1000):
            continue
        values[count] = (int(import_val_fetch.json()[x][2]))/1000000
        countries[count] = (import_val_fetch.json()[x][4])
        count = count + 1
    
    # 
    sorted_trade_values = list(zip(values, countries))
    real_sorted_trade_values = sorted(sorted_trade_values, key = lambda x: x[0])
    sorted_values = [i[0] for i in real_sorted_trade_values]
    sorted_countries = [i[1] for i in real_sorted_trade_values]
    print(sorted_countries)
    print(sorted_values)
    amount_print = size(sorted_values)
        
    plt.bar(sorted_countries, sorted_values)
    plt.xticks(rotation = 90)
    title = "US imports of " + commodity_item + " in " + year + " by partner"
    plt.title(title)
    plt.ylabel("Imports (CIF) in USD millions")
    plt.xlabel("Import Country of Origin")
    plt.show()

def country_item_value():
    print("Hi")
    year = input("Enter your desired year: ")
    hs_commodity_code = input("Enter your desired HS commodity code: ")
    country_code = input("Enter your desired country code: ")
    URL_base = 'https://api.census.gov/data/timeseries/intltrade/imports/hs?get=I_COMMODITY,I_COMMODITY_LDESC,GEN_CIF_YR&'
    time_base = 'time=' + year + "-12"
    country_base = "&CTY_CODE=" + country_code
    URL_fetch = URL_base + time_base + country_base
    print(URL_fetch)
#https://api.census.gov/data/timeseries/intltrade/imports/hs?get=I_COMMODITY,I_COMMODITY_LDESC,GEN_VAL_MO&time=2017-01&I_COMMODITY=848620&CTY_CODE=1220
#https://api.census.gov/data/timeseries/intltrade/imports/hs?get=I_COMMODITY,I_COMMODITY_LDESC,GEN_VAL_MO,CTY_NAME&time=2017-01&I_COMMODITY=848620&CTY_CODE=2010
#def product_country_time():
    # This is an example of
    # US imports from Japan broken down by 4 digit code
    #https://api.census.gov/data/timeseries/intltrade/imports/hs?get=I_COMMODITY,I_COMMODITY_LDESC,GEN_CIF_YR&time=2017-12&CTY_CODE=5880
#def drop_down_menus():
#    print("Hi")


def main():
    master = tkr.Tk()
    master.geometry("200x100")
    master.title("Dropdown List")

    
    tkr.Label(master, text = "Countries").grid(row = 0)
    clicked = tkr.StringVar()
    clicked.set("Canada")
    set1 = tkr.OptionMenu(master, clicked, "Canada", "Mexico", "Japan", "Germany", "China")


    set1.configure(font=("Arial", 25))
    set1.grid(row = 1, column = 0)


    tkr.mainloop()
    country_import = clicked.get()
    print(country_import)

    country_code_values = 0
    if(country_import == "Canada"):
        country_code_values = 1220
    
    elif(country_import == "Mexico"):
        country_code_values = 2010
    
    elif(country_import == "Japan"):
        country_code_values = 5880
    
    elif(country_import == "Germany"):
        country_code_values = 4280
    
    elif(country_import == "China"):
        country_code_values = 5700
    print(type(country_code_values))
    country_imports(country_code_values)
main()

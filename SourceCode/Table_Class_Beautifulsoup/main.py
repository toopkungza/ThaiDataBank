# -*- coding: utf-8 -*-
"""
#Infomation Scraper - Thai School Information
#Code for scraping data from table

Created on Sun Jul 17 22:00:14 2022

@author: tkz

REFERENCE: https://stackoverflow.com/questions/38155206/scrape-a-table-class-in-python
REFERENCE2: https://www.adamsmith.haus/python/answers/how-to-create-pandas-dataframe-from-a-numpy-array-in-python

DATA SOURCE: https://www.spu.ac.th/directory/school/

All the credits go to Sripatum University for the origin of data
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def ContentGraber(source):
    
    # ---- SET PARAMETERS ----
    TableClassLocator = "table table-bordered table-school-1" #>> for school data extraction

    # ---- Getting content of the website ---- #
    HTMLCode = requests.get(source).content
    HTMLinSoup = BeautifulSoup(HTMLCode)
    TableinSoup = HTMLinSoup.find('table', {'class': TableClassLocator})
    
    #Data Extraction! Let's begin.
    container = []
    
    for elem in TableinSoup.find_all("tr"):                 #find what is in tr class
        textcolumn1, textcolumn2 = elem.find_all("td")      #locate text in td class
        container.append(textcolumn2.text)
    return container

def URLGraber(source):
    
    # ---- SET PARAMETERS ----
    TableClassLocator = "table table-striped table-school-1" #>> for school url extraction from main site

    # ---- Getting content of the website ---- #
    HTMLCode = requests.get(source).content
    HTMLinSoup = BeautifulSoup(HTMLCode)
    TableinSoup = HTMLinSoup.find('table', {'class': TableClassLocator})
    
    #Data Extraction! Let's begin.
    container = []
    
    for elem in TableinSoup.find_all("tr"):                 #find what is in tr class
        textcolumn1 = elem.find("a")      #locate text in td class.
        container.append("https://www.spu.ac.th" + textcolumn1['href'])
    return container

def URLCorrection(urllist):
    ErrorChkIndexDict = {}
    correction = []
    
    for i in range(len(urllist)):
        if urllist[i].find("/http") != -1:
            ErrorChkIndexDict[i] = (urllist[i].find("/http")) + 1
    for elem in ErrorChkIndexDict:
        correction.append(urllist[elem][ErrorChkIndexDict[elem]:])
        urllist[elem] = urllist[elem][0:ErrorChkIndexDict[elem]]
    for elem in correction:
        urllist.append(elem)
    return urllist
    
#PHASE 1 ---- URL Extraction ----
"""
urlfull = []
ContainerAll = []
for i in range(0, 5):
    urlroot = "https://www.spu.ac.th/directory/school/province/78/?id=78&do=province&page=" + str(i+1)
    urlfull.append(urlroot)
    
for elem in urlfull:
    ContainerAll.extend(URLGraber(elem))
    
with open("/home/tkz/Desktop/CodingProjects/Project1.txt", "a+") as file:
    file.write('\n'.join(ContainerAll))

"""
#PHASE 2 ---- Data Extraction and DataFrame Creation ----

with open("/home/tkz/Desktop/CodingProjects/Project1.txt", "r") as file:
    sourcelist = file.readlines()
    
DataURL = []
for elem in sourcelist:
    DataURL.append(elem[:-1])
if len(sourcelist) == len(DataURL):
    print("Complete!")
else:
    print("Length of data is not the same. There may be some inconsistency in the data between the end character deletion.")
URLCorrection(DataURL)

ContainerAll = []
for elem in DataURL:
    ContainerAll.append(ContentGraber(elem))
    time.sleep(random.random())

#Create DataFrame from ContainerAll
df = pd.DataFrame(data=ContainerAll, columns=["SCHOOLNAME", "AUTHORITY", "SCHOOLTYPE", "THCITY", "THDISTRICT", "THPROVINCE", "EMAIL", "WEBSITE"])

#PHASE 3 ---- Data Clean-up (if necessary) :-P


#PHASE FINAL
#Export to .csv file for data import"""
import glob
import os
import json
import configparser
import re
import time
from datetime import date

import pandas as pandas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4

# Initialize variables
# Windows PC:
PATH = "./drivers/chromedriver.exe"

# LINUX PC:
# PATH = "./drivers/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(PATH, options=chrome_options)
google_url = "https://www.google.be/search?q=artificiële intelligentie bedrijf"
googleLinkedin_url = "https://www.google.be/search?q=linkedin"
driver.get(google_url)

dataJSON = {'resultData': []}


# FUNCTIONS

# Returns name from site URL
def getNameFromSiteURL(url):
    length = len(url.split("."))
    if length == 2:
        firstElLink = url.split(".")[0]
        name = firstElLink.split("/")[2]
    else:
        name = url.split(".")[1]
    return str(name)

# SCRIPT

# Remove Agree button and grayed out background
# jsname = "bF1uUb"
# driver.execute_script("document.querySelector('[jsname=" + jsname + "]').style.display = 'none'")
# className = "bErdLd aID8W wwYr3"
# driver.execute_script("document.getElementsByClassName('" + className + "')[0].style.display = 'none'")
# driver.execute_script("document.getElementsByTagName('html')[0].style.overflow = 'auto'")

#
# # Remove old contents screenshot folder
# files = glob.glob('./screenshots/*')
# for f in files:
#     os.remove(f)

# GET ALL LINKS
# Get ad links
adLinks = []
for el in driver.find_elements_by_class_name("Krnil"):
    adLinks.append(el.get_attribute('href'))

    # Add company name to JSON file
    # addNameFromURLToJson(str(el.get_attribute('href')), True, dataJSON)

# Get 4 first search results
rLinks = []
results = driver.find_elements_by_class_name("g")
for i in range(4):
    rLinks.append(results[i].find_element_by_tag_name("a").get_attribute('href'))

    # Add name site to JSON
    # (str(results[i].find_element_by_tag_name("a").get_attribute('href')), False, dataJSON)




# Load previous data (Should be replaces with a database)
# with open("./data/WebscrapeData.json") as jsData:
#     global scraper_df
#     scraper_df = pandas.read_json(jsData, orient='table')
#     print(scraper_df)
#     jsData.close()


# Add LinkedIn info to DF
def addLinkedinToDF(url, scraperCat):
    name = str(getNameFromSiteURL(url))
    driver.get(googleLinkedin_url + name)
    linkedInLink = str(driver.find_elements_by_class_name("g")[0].find_element_by_tag_name("a").get_attribute('href'))
    length = len(linkedInLink.split("/"))
    linkedInName = linkedInLink.split("/")[length - 1]
    # Add categories
    driver.get("https://www.linkedin.com/company/" + linkedInName + "/about/")
    driver.implicitly_wait(2)
    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
    categories = []
    if str(soup.find(text=re.compile('Specialismen'))) != "None":
        print('appended Cat')
        categories = str(soup.find(text=re.compile('Specialismen')).parent.findNext('dd').contents[0]) \
            .strip().split(",")
        lastCategory = categories.pop()
        # Check if last category contains 'en' and split
        if " en " in str(lastCategory):
            categories.pop()
            categories.append(lastCategory.split(" en ")[0].strip())
            categories.append(lastCategory.split(" en ")[1].strip())

    # Add jobs
    driver.get("https://www.linkedin.com/company/" + linkedInName + "/jobs/")
    driver.implicitly_wait(3)
    jobTitles = []
    if len(driver.find_elements_by_class_name("org-jobs-empty-jobs-module__computer-illustration illustration-56")) \
            == 0:
        jobElements = driver.find_elements_by_class_name("job-card-square__title")
        for elm in jobElements:
            title = str(elm.text).replace('Functietitel\n', '')
            if title != "":
                jobTitles.append(title)

    data = [[name, scraperCat, jobTitles, categories, date.today().strftime("%d/%m/%Y")]]
    df_el = pandas.DataFrame(data=data, columns=['Name', 'ScraperCategory', 'Jobs', 'Category', 'Date'])
    global scraper_df
    scraper_df = scraper_df.append(df_el, ignore_index=True)
    print('appended')


# GET LINKEDIN DATA COMPANIES
# Initialize LinkedIn with local account details
# (create your own config.ini with account details local and point to that path)
accountDetailsConfig = configparser.ConfigParser()
#accountDetailsConfig.read('C:/Users/Maarten Van den hof/Documents/config.ini')
accountDetailsConfig.read('C:/Users/maart/Documents/config.ini')
driver.get("https://www.linkedin.com/")
driver.find_element_by_id("session_key").send_keys(accountDetailsConfig['CREDS']['USERNAME'])
driver.find_element_by_id("session_password").send_keys(accountDetailsConfig['CREDS']['PASSWORD'])
driver.find_elements_by_class_name("sign-in-form__submit-button")[0].click()
print('wait')
time.sleep(10)

scraper_df = pandas.DataFrame(columns=['Name', 'ScraperCategory', 'Jobs', 'Category', 'Date'])
# Get linkedin links
for link in adLinks:
    addLinkedinToDF(link, "advertisement")
for link in rLinks:
    addLinkedinToDF(link, "search result")

print(scraper_df)

# Write JSON file
with open('./data/WebscrapeData.json', 'w') as out:
    parsed = json.loads(scraper_df.to_json(orient="table"))
    json.dump(parsed, out, indent=4)

# Close browser
driver.quit()

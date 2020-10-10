import glob
import os
import json
import configparser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize variables
# Windows PC:
PATH = "C:/Program Files (x86)/chromedriver.exe"

# LINUX PC:
# PATH = "./drivers/chromedriver"

chrome_options = Options()


driver = webdriver.Chrome(PATH, options=chrome_options)
google_url = "https://www.google.be/search?q=artificiële intelligentie bedrijf"
googleLinkedin_url = "https://www.google.be/search?q=linkedin"
driver.get(google_url)

dataJSON = {'adCompanies': [], 'searchResults': []}


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


# Screenshot function
def screenshotURLAndAddPathToJSON(url, screenshotName, orgName, isCompany, jsonFile, pathType):
    # Set height
    driver.get(url)
    htmlTag = driver.find_element_by_tag_name('html')
    height = htmlTag.size["height"] + 1000
    driver.set_window_size(1920, height)

    # Take Screenshot
    driver.save_screenshot("screenshots/" + screenshotName + '.png')
    print("screenshot " + screenshotName + " taken")

    # Save path to JSON
    if isCompany:
        for element in jsonFile['adCompanies']:
            if element['name'] == orgName:
                element[str(pathType)] = 'screenshots/' + screenshotName + '.png'
                break
    else:
        for element in jsonFile['searchResults']:
            if element['name'] == orgName:
                element[str(pathType)] = 'screenshots/' + screenshotName + '.png'
                break


# Returns the name of the company from the URL
def addNameFromURLToJson(url, isCompany, jsonFile):
    name = getNameFromSiteURL(url)
    if isCompany:
        jsonFile['adCompanies'].append({
            'name': name
        })
    else:
        jsonFile['searchResults'].append({
            'name': name
        })


# Add LinkedIn page to JSON
def addLinkedinToJSON(url):
    name = str(getNameFromSiteURL(url))
    driver.get(googleLinkedin_url + name)
    linkedinLink = driver.find_elements_by_class_name("g")[0].find_element_by_tag_name("a").get_attribute('href')
    screenshotURLAndAddPathToJSON(linkedinLink, "linkedinScreenshot_" + name, name
                                  , True, dataJSON, "linkedinScreenshot")


# SCRIPT

# Remove Agree button and grayed out background
# jsname = "bF1uUb"
# driver.execute_script("document.querySelector('[jsname=" + jsname + "]').style.display = 'none'")
# className = "bErdLd aID8W wwYr3"
# driver.execute_script("document.getElementsByClassName('" + className + "')[0].style.display = 'none'")
# driver.execute_script("document.getElementsByTagName('html')[0].style.overflow = 'auto'")

# Remove old contents screenshot folder
files = glob.glob('./screenshots/*')
for f in files:
    os.remove(f)


# GET ALL LINKS
# Get ad links
adLinks = []
for el in driver.find_elements_by_class_name("Krnil"):
    adLinks.append(el.get_attribute('href'))

    # Add company name to JSON file
    addNameFromURLToJson(str(el.get_attribute('href')), True, dataJSON)

# Get 4 first search results
rLinks = []
results = driver.find_elements_by_class_name("g")
for i in range(4):
    rLinks.append(results[i].find_element_by_tag_name("a").get_attribute('href'))

    # Add name site to JSON
    addNameFromURLToJson(str(results[i].find_element_by_tag_name("a").get_attribute('href')), False, dataJSON)


# NAVIGATE TO AND TAKE SCREENSHOTS FROM SITES
# Take screenshot ad pages and save URL's to txt file
index = 0
for url in adLinks:
    index = index + 1
    screenshotURLAndAddPathToJSON(url, "adScreenshot_" + str(index), str(getNameFromSiteURL(url)),
                                  True, dataJSON, "screenshotPath")

# Take screenshot search results
index = 0
for url in rLinks:
    index = index + 1
    screenshotURLAndAddPathToJSON(url, "resultScreenshot_" + str(index), str(getNameFromSiteURL(url)),
                                  False, dataJSON, "screenshotPath")


# GET LINKEDIN DATA COMPANIES
# Initialize LinkedIn
config = configparser.ConfigParser()
config.read('C:/Users/maart/Documents/config.ini')
driver.get("https://www.linkedin.com/")
driver.find_element_by_id("session_key").send_keys(config['CREDS']['USERNAME'])
driver.find_element_by_id("session_password").send_keys(config['CREDS']['PASSWORD'])
driver.find_elements_by_class_name("sign-in-form__submit-button")[0].click()

# Get linkedin links
for link in adLinks:
    addLinkedinToJSON(link)
for link in rLinks:
    addLinkedinToJSON(link)

# Write JSON file
with open('./data/WebscrapeData.json', 'w') as out:
    json.dump(dataJSON, out)

# Close browser
driver.quit()

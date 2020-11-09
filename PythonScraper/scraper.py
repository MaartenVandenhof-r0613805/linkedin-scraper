import glob
import os
import json
import configparser
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import bs4

# Initialize variables
# Windows PC:
PATH = "C:/Program Files (x86)/chromedriver.exe"

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


# Screenshot function
def screenshotURLAndAddPathToJSON(url, screenshotName, orgName, jsonFile, pathType):
    # Set height
    driver.get(url)
    htmlTag = driver.find_element_by_tag_name('html')
    height = htmlTag.size["height"] + 1000
    driver.set_window_size(1920, height)

    # Agree to cookies
    driver.implicitly_wait(5)
    buttonNames = ["proceed", "agree", "aanvaard", "accepteer", "accepteren", "accept", "akkoord"]
    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
    for name in buttonNames:
        if soup.findAll('button', text=re.compile(".*" + name + ".*")):
            for element in soup.findAll('button', text=re.compile(".*" + name + ".*")):
                try:
                    driver.find_element_by_id(element.get("id")).click()
                except:
                    print("cookiebutton not found by id")

    # Take Screenshot
    driver.save_screenshot("screenshots/" + screenshotName + '.png')
    print("screenshot " + screenshotName + " taken")

    # Save path to JSON
    for element in jsonFile['resultData']:
        if element['name'] == orgName:
            element[str(pathType)] = 'screenshots/' + screenshotName + '.png'
            break


# Returns the name of the company from the URL
def addNameFromURLToJson(url, isCompany, jsonFile):
    name = getNameFromSiteURL(url)
    if isCompany:
        jsonFile['resultData'].append({
            'name': name,
            'resultCategory': 'adCompany'
        })
    else:
        jsonFile['resultData'].append({
            'name': name,
            'resultCategory': 'searchResults'
        })


# Add element to Json
def addElementToJson(name, elementName, element, jsonFile):
    for elm in jsonFile['resultData']:
        if elm['name'] == name:
            elm[str(elementName)] = element


# Add LinkedIn info to JSON
def addLinkedinToJSON(url):
    name = str(getNameFromSiteURL(url))
    driver.get(googleLinkedin_url + name)
    linkedInLink = str(driver.find_elements_by_class_name("g")[0].find_element_by_tag_name("a").get_attribute('href'))
    length = len(linkedInLink.split("/"))
    linkedInName = linkedInLink.split("/")[length - 1]
    # Take screenshot homepage
    screenshotURLAndAddPathToJSON(linkedInLink, "linkedinScreenshot_" + name, name
                                  , dataJSON, "linkedinScreenshot")
    # Add categories
    driver.get("https://www.linkedin.com/company/" + linkedInName + "/about/")
    driver.implicitly_wait(2)
    soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
    if str(soup.find(text=re.compile('Specialismen'))) != "None":
        categories = str(soup.find(text=re.compile('Specialismen')).parent.findNext('dd').contents[0]) \
            .strip().split(",")
        lastCategory = categories.pop()
        # Check if last category contains en and split
        if " en " in str(lastCategory):
            categories.pop()
            categories.append(lastCategory.split(" en ")[0].strip())
            categories.append(lastCategory.split(" en ")[1].strip())
        addElementToJson(name, "categories", categories, dataJSON)

    # Add jobs
    driver.get("https://www.linkedin.com/company/" + linkedInName + "/jobs/")
    driver.implicitly_wait(2)
    if len(driver.find_elements_by_class_name("org-jobs-empty-jobs-module__computer-illustration illustration-56")) \
            == 0:
        jobElements = driver.find_elements_by_class_name("job-card-square__title")
        jobTitles = []
        for elm in jobElements:
            title = str(elm.text).replace('Functietitel\n', '')
            if title != "":
                jobTitles.append(title)
        addElementToJson(name, "jobs", jobTitles, dataJSON)


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
for link in adLinks:
    index = index + 1
    screenshotURLAndAddPathToJSON(link, "adScreenshot_" + str(index), str(getNameFromSiteURL(link))
                                  , dataJSON, "screenshotPath")

# Take screenshot search results
index = 0
for link in rLinks:
    index = index + 1
    screenshotURLAndAddPathToJSON(link, "resultScreenshot_" + str(index), str(getNameFromSiteURL(link)),
                                  dataJSON, "screenshotPath")

# GET LINKEDIN DATA COMPANIES
# Initialize LinkedIn with local account details
# (create your own config.ini with account details local and point to that path)
accountDetailsConfig = configparser.ConfigParser()
accountDetailsConfig.read('C:/Users/maart/Documents/config.ini')
driver.get("https://www.linkedin.com/")
driver.find_element_by_id("session_key").send_keys(accountDetailsConfig['CREDS']['USERNAME'])
driver.find_element_by_id("session_password").send_keys(accountDetailsConfig['CREDS']['PASSWORD'])
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

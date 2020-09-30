import glob
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Initialize variables
# Windows PC:
PATH = "C:/Program Files (x86)/chromedriver.exe"

# LINUX PC:
# PATH = "./drivers/chromedriver"

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(PATH, options=chrome_options)
google_url = "https://www.google.be/search?q=artificiële intelligentie bedrijf"
driver.get(google_url)


# FUNCTIONS

# Screenshot function
def screenshotURL(url, name):
    # Set height
    driver.get(url)
    htmltag = driver.find_element_by_tag_name('html')
    height = htmltag.size["height"] + 1000
    driver.set_window_size(1920, height)

    # Take Screenshot
    driver.save_screenshot("screenshots/" + name + '.png')
    print("screenshot " + name + " taken")


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

# Get ad links
adLinks = []
for el in driver.find_elements_by_class_name("Krnil"):
    adLinks.append(el.get_attribute('href'))

# Get 4 first search results
rLinks = []
results = driver.find_elements_by_class_name("g")
for i in range(4):
    rLinks.append(results[i].find_element_by_tag_name("a").get_attribute('href'))

# Take screenshot ad pages and save URL's to txt file
file = open("adURLs.txt", "w+")
index = 0
for el in adLinks:
    index = index + 1
    file.write(el + '\n')
    screenshotURL(el, "adScreenshot_" + str(index))
file.close()

# Take screenshot search results
index = 0
for el in rLinks:
    index = index + 1
    screenshotURL(el, "resultScreenshot_" + str(index))

# Close browser
driver.quit()

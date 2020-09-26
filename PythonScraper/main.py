from selenium import webdriver

# Initialize variables
PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)
google_url = "https://www.google.be/search?q=artificiële intelligentie bedrijf"
driver.get(google_url)


# FUNCTIONS

# Screenshot function
def screenshotURL(url, name):
    # Set height
    driver.get(url)
    htmlTag = driver.find_element_by_tag_name('html')
    height = htmlTag.size["height"] + 1000
    driver.set_window_size(1920, height)

    # Take Screenshot
    driver.save_screenshot(name + '.png')


# SCRIPT

# Remove Agree button and grayed out background
jsname = "bF1uUb"
driver.execute_script("document.querySelector('[jsname=" + jsname + "]').style.display = 'none'")
className = "bErdLd aID8W wwYr3"
driver.execute_script("document.getElementsByClassName('" + className + "')[0].style.display = 'none'")
driver.execute_script("document.getElementsByTagName('html')[0].style.overflow = 'auto'")

# Get ad links
adLinks = []
for el in driver.find_elements_by_class_name("Krnil"):
    adLinks.append(el.get_attribute('href'))

# Take screenshot and save URL's to txt file
file = open("adURLs.txt", "w+")
index = 0
for el in adLinks:
    index = index + 1
    file.write(el + '\n')
    screenshotURL(el, "screenshot_" + str(index))

file.close()

# Close browser
driver.quit()
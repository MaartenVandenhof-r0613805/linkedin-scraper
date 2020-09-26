from selenium import webdriver

PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

google_url = "https://www.google.be/search?q=artificiële intelligentie bedrijf"
driver.get(google_url)

# Remove Agree button and grayed out background
jsname = "bF1uUb"
driver.execute_script("document.querySelector('[jsname=" + jsname + "]').style.display = 'none'")
className = "bErdLd aID8W wwYr3"
driver.execute_script("document.getElementsByClassName('" + className + "')[0].style.display = 'none'")
driver.execute_script("document.getElementsByTagName('html')[0].style.overflow = 'auto'")

# Get ad links
addElements = driver.find_elements_by_class_name("Krnil")
file = open("adURLs.txt", "w+")
for el in addElements:
    file.write(el.get_attribute('href') + '\n')

file.close()

# Close browser
driver.close()
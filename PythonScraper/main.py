from selenium import webdriver

PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)

google_url = "https://www.google.com/search?q=python" + "&num=" + str(5)
driver.get(google_url)

# Remove Agree button and grayed out background
jsname = "bF1uUb"
driver.execute_script("document.querySelector('[jsname=" + jsname + "]').style.display = 'none'")
className = "bErdLd aID8W wwYr3"
driver.execute_script("document.getElementsByClassName('" + className + "')[0].style.display = 'none'")

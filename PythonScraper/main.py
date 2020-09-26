from selenium import webdriver


PATH = "C:/Program Files (x86)/chromedriver.exe"
driver = webdriver.Chrome(PATH)


google_url = "https://www.google.com/search?q=python" + "&num=" + str(5)
driver.get(google_url)

grayArea = driver.find_element_by_xpath('//div[@jsname="bF1uUb"]')
driver.execute_script("document.querySelector('[jsname='bF1uUb']').style.display = 'none'")

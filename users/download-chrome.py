from selenium import webdriver

"""
A Download ChromeDriver written by python
"""

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless=new')

driver = webdriver.Chrome(options=chrome_options)

driver.quit()

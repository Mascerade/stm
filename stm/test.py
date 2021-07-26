from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

opts = chrome.options.Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
opts.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome('./chromedriver', options=opts)
driver.get('https://www.walmart.com/')
driver.execute_script('''window.open("https://www.amazon.com/", "_blank");''')
driver.execute_script('''window.open("https://www.newegg.com/", "_blank");''')
print(driver.window_handles)
driver.switch_to.window(driver.window_handles[0])

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'header-bubble-links'))
    )
    print(element)
except:
    print('timeout')

#driver.quit()
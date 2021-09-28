from stm.manager import ChromeTabManager
from stm.tab import Tab
from selenium.webdriver import chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By

# Be able to manipulate the page right when we arrive on it
caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'none'

# Add Chrome options to change the user agent and get rid of the "Chrome is being automated" message.
opts = chrome.options.Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
opts.add_experimental_option('excludeSwitches', ['enable-automation'])

# Create the tabs to use and create the manager
tab1 = Tab('Amazon', 'https://www.amazon.com/', indicator_element=(By.ID, 'navbar'))
tab2 = Tab('Google', 'https://www.google.com/', indicator_element=(By.CLASS_NAME, 'L3eUgb'))
tab3 = Tab('Apple', 'https://www.apple.com/', indicator_element=(By.ID, 'ac-globalnav'))
tab4 = Tab('Apple', 'https://www.apple.com/', implicit_wait=10)
manager = ChromeTabManager(tabs=[tab1, tab2, tab3, tab4],
                        executable_path='./bin/chromedriver',
                        desired_capabilities=caps,
                        options=opts)

# Open all the tabs that were added on the manager's initialization
manager.open_tabs()
page_sources = manager.execute_all_on_indicated()

# Confirm that getting the page sources worked.
for key, value in page_sources.items():
    print(key, value[:100])
    print('________________________________')
manager.quit()

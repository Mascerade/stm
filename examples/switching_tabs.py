from stm.manager import ChromeTabManager
from stm.tab import Tab
from time import sleep
from selenium.webdriver import chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

'''
Example of how the tab manager can be used to easily switch between tabs.
'''

# So that driver.get() doesn't wait for the page to load
caps = DesiredCapabilities().CHROME
caps['pageLoadStrategy'] = 'none'

# Add Chrome options to change the user agent and get rid of the "Chrome is being automated" message.
opts = chrome.options.Options()
opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
opts.add_experimental_option('excludeSwitches', ['enable-automation'])

# Create the tabs to use and create the manager
tab1 = Tab('GitHub', 'https://www.github.com/')
tab2 = Tab('Google', 'https://www.google.com/')
tab3 = Tab('Apple', 'https://www.apple.com/')
manager = ChromeTabManager(tabs=[tab1, tab2, tab3],
                        executable_path='./bin/chromedriver',
                        desired_capabilities=caps,
                        options=opts)

# Open all the tabs that were added on the manager's initialization
manager.open_tabs()
sleep(1)

# Test switch tab forward
print('Switching tabs forward')
manager.switch_tab_forward()
sleep(1)
manager.switch_tab_forward()
sleep(1)
manager.switch_tab_forward()
sleep(1)
manager.switch_tab_forward()
sleep(1)

# Test switch by specific tabs
print('Switching tabs by object')
manager.switch_to_tab_by_obj(tab2)
sleep(1)
manager.switch_to_tab_by_obj(tab3)
sleep(1)
manager.switch_to_tab_by_obj(tab1)
sleep(3)

# Destroy the manager (closing the browser window)
manager.quit()

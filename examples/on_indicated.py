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
tab1 = Tab('BestBuy Wait Page Load', 'https://www.bestbuy.com/site/searchpage.jsp?st=intel+core+i7&_dyncharset=UTF-8&_dynSessConf=&id=pcat17071&type=page&sc=Global&cp=1&nrp=&sp=&qp=&list=n&af=true&iht=y&usc=All+Categories&ks=960&keys=keys', wait_page_load=True, max_wait=10, load_type='complete')
tab2 = Tab('Amazon', 'https://www.amazon.com/', indicator_element=(By.ID, 'navbar'))
tab3 = Tab('Google', 'https://www.google.com/', indicator_element=(By.CLASS_NAME, 'L3eUgb'))
tab4 = Tab('Apple', 'https://www.apple.com/', indicator_element=(By.ID, 'ac-globalnav'))
tab5 = Tab('Apple Explicit Wait', 'https://www.apple.com/', explicit_wait=10)
manager = ChromeTabManager(tabs=[tab5, tab2, tab3, tab4, tab1],
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

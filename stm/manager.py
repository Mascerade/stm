from typing import List, Optional
from tab import Tab
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeManager(webdriver.Chrome):
    def __init__(self, tabs: List[Tab], *args, **kwargs):
        super(ChromeManager, self).__init__(*args, **kwargs)
        self.tabs = tabs
        self.currentTab: Optional[str] = None
        self.newTabScript = '''window.open("{}", "_blank");'''

    def __openTab(self, tab: Tab) -> None:
        '''
        Opens given tab.
        '''
        self.execute_script(self.newTabScript.format(tab.url))
        # Set the tab's handle to the latest one added (so this tab)
        tab.setHandle(self.window_handles[-1])
    
    def __findTabByName(self, tabName: str) -> Optional[Tab]:
        '''
        Returns a Tab object if a tab in the list matches the name given.
        Otherwise, return None.
        '''
        for tab in self.tabs:
            if tab.name == tabName:
                return tab
        
        return None

    def openTabByName(self, tabName: str) -> None:
        '''
        Opens a tab that is already added to the manager by the name of it.
        '''
        tab = self.__findTabByName(tabName)
        if tab is not None:
            self.__openTab(tab)

    def openTabs(self) -> None:
        '''
        Open the tabs passed in through the tab argument.
        '''
        for tab in self.tabs:
            self.__openTab(tab)

    def addTab(self, name: str, url: str, indicatorElement: Optional[str]) -> None:
        '''
        Add a tab to the list of tabs.
        '''
        nTab = Tab(name, url, indicatorElement)
        self.tabs.append(nTab)
    

if __name__ == '__main__':
    from time import sleep

    # Add Chrome options to change the user agent and get rid of the "Chrome is being automated" message.
    opts = chrome.options.Options()
    opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    opts.add_experimental_option('excludeSwitches', ['enable-automation'])

    # Create the tabs to use and create the manager
    tab1 = Tab('Walmart', 'https://www.github.com/')
    tab2 = Tab('Amazon', 'https://www.google.com/')
    tab3 = Tab('Newegg', 'https://www.apple.com/')
    driver = ChromeManager(tabs=[tab1, tab2, tab3],
                           executable_path='./chromedriver',
                           options=opts)
    driver.openTabs()
    sleep(5)
    driver.quit()

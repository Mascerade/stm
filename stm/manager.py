from typing import List, Optional
from stm.tab import Tab
from time import sleep
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeTabManager(webdriver.Chrome):
    def __init__(self, tabs: List[Tab], *args, **kwargs):
        super(ChromeTabManager, self).__init__(*args, **kwargs)
        self.addedTabs: List[Tab] = []
        self.openedTabs: List[Tab] = []
        self.currentTab: Optional[Tab] = None
        self.newTabScript = '''window.open("{}", "_blank");'''

        for tab in tabs:
            tab.setManager(self)
            self.addedTabs.append(tab)
        
    def __indexOfTab(self, locTab: Tab) -> Optional[int]:
        '''
        Gets the index of a given tab in the tab list.
        '''
        for idx, tab in enumerate(self.addedTabs):
            if tab is locTab:
                return idx
        
        return None

    def __findTabByName(self, tabName: str) -> Optional[Tab]:
        '''
        Returns a Tab object if a tab in the list matches the name given.
        Otherwise, return None.
        '''
        for tab in self.addedTabs:
            if tab.name == tabName:
                return tab
        
        return None
    
    def __setOpenedTabInfo(self, tab: Tab) -> None:
        '''
        Adds the necessary information to a newly opened tab including:
          The handle assigned to it
          The position it is at in the browser (according to the order).
        Also sets the opened tab to the current tab
        '''
        self.openedTabs.append(tab)
        tab.setHandle(self.window_handles[-1])
        tab.setPosition(len(self.openedTabs) - 1)
        self.currentTab = tab

    def __openFirstTab(self, tab: Tab) -> None:
        '''
        First tab is special because we have to use "get" function instead of newTabScript
        '''
        print('here in openFirstTab')
        self.execute_script(self.newTabScript.format(tab.url))
        self.switch_to.window(self.window_handles[0])
        self.close()
        self.__setOpenedTabInfo(tab)
        self.switch_to.window(tab.handleName)
        print('end of openFirstTab')

    def __openNewTab(self, tab: Tab) -> None:
        '''
        Opens given tab.
        '''
        self.execute_script(self.newTabScript.format(tab.url))
        self.__setOpenedTabInfo(tab)

    def openTabs(self) -> None:
        '''
        Open tabs that are unopened, but added.
        '''
        for tab in self.addedTabs:
            if tab.handleName is None:
                print(f'Opened Tabs: {self.openedTabs}')
                if len(self.openedTabs) == 0:
                    self.__openFirstTab(tab)
                    print('here after open')
                else:
                    self.__openNewTab(tab)

    def addNewTab(self, tab: Tab) -> None:
        '''
        Add a tab and assign it the manager.
        '''
        self.addedTabs.append(tab)
        tab.setManager(self)

    def switchTabForward(self):
        '''
        Switch to the next tab.
        '''
        if self.currentTab.position == len(self.openedTabs) -1:
            self.currentTab = self.openedTabs[0]
        else:
            self.currentTab = self.openedTabs[self.currentTab.position + 1]
        
        self.switch_to.window(self.currentTab.handleName)

    def switchToTabByObj(self, tab: Tab) -> None:
        '''
        Switch to a specific tab.
        '''
        if tab.handleName is not None and tab.manager is self and self.currentTab is not tab:
            self.currentTab = tab
            self.switch_to.window(self.currentTab.handleName)

        else:
            print('Tab is either not part of this manager or is not open!')


if __name__ == '__main__':
    caps = DesiredCapabilities().CHROME
    caps['pageLoadStrategy'] = 'none'

    # Add Chrome options to change the user agent and get rid of the "Chrome is being automated" message.
    opts = chrome.options.Options()
    opts.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36')
    opts.add_experimental_option('excludeSwitches', ['enable-automation'])

    # Create the tabs to use and create the manager
    tab1 = Tab('Walmart', 'https://www.github.com/')
    tab2 = Tab('Amazon', 'https://www.google.com/')
    tab3 = Tab('Newegg', 'https://www.apple.com/')
    driver = ChromeTabManager(tabs=[tab1, tab2, tab3],
                           executable_path='./chromedriver',
                           desired_capabilities=caps,
                           options=opts)
    driver.openTabs()
    sleep(5)
    driver.quit()

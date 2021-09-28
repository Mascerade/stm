from typing import Dict, Any, List, Optional
from stm.tab import Tab
from time import sleep
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ChromeTabManager(webdriver.Chrome):
    '''
    Wrapper around the Chrome WebDriver that is able to handle opening
    multiple tabs.
    '''
    
    def __init__(self, tabs: List[Tab], *args, **kwargs):
        super(ChromeTabManager, self).__init__(*args, **kwargs)
        self.added_tabs: List[Tab] = []
        self.opened_tabs: List[Tab] = []
        self.current_tab: Optional[Tab] = None
        self.newTabScript = '''window.open("{}", "_blank");'''

        for tab in tabs:
            tab.set_manager(self)
            self.added_tabs.append(tab)
        
    def __index_of_tab(self, locTab: Tab) -> Optional[int]:
        '''
        Gets the index of a given tab in the tab list.
        '''
        for idx, tab in enumerate(self.added_tabs):
            if tab is locTab:
                return idx
        
        return None

    def __find_tab_by_name(self, tabName: str) -> Optional[Tab]:
        '''
        Returns a Tab object if a tab in the list matches the name given.
        Otherwise, return None.
        '''
        for tab in self.added_tabs:
            if tab.name == tabName:
                return tab
        
        return None
    
    def __set_opened_tab_info(self, tab: Tab) -> None:
        '''
        Adds the necessary information to a newly opened tab including:
          The handle assigned to it
          The position it is at in the browser (according to the order).
        Also sets the opened tab to the current tab
        '''
        self.opened_tabs.append(tab)
        tab.set_handle(self.window_handles[-1])
        tab.set_position(len(self.opened_tabs) - 1)
        self.current_tab = tab

    def __open_first_tab(self, tab: Tab) -> None:
        '''
        First tab is special because we have to use "get" function instead of newTabScript
        '''
        self.execute_script(self.newTabScript.format(tab.url))
        self.switch_to.window(self.window_handles[0])
        self.close()
        self.__set_opened_tab_info(tab)
        self.switch_to.window(tab.window_handle)

    def __open_new_tab(self, tab: Tab) -> None:
        '''
        Opens given tab.
        '''
        self.execute_script(self.newTabScript.format(tab.url))
        self.__set_opened_tab_info(tab)

    def open_tabs(self) -> None:
        '''
        Open tabs that are unopened, but added.
        '''
        for tab in self.added_tabs:
            if tab.window_handle is None:
                if len(self.opened_tabs) == 0:
                    self.__open_first_tab(tab)
                else:
                    self.__open_new_tab(tab)

    def add_new_tab(self, tab: Tab) -> None:
        '''
        Add a tab and assign it the manager.
        '''
        self.added_tabs.append(tab)
        tab.set_manager(self)

    def switch_tab_forward(self):
        '''
        Switch to the next tab.
        '''
        if self.current_tab.position == len(self.opened_tabs) -1:
            self.current_tab = self.opened_tabs[0]
        else:
            self.current_tab = self.opened_tabs[self.current_tab.position + 1]
        
        self.switch_to.window(self.current_tab.window_handle)

    def switch_to_tab_by_obj(self, tab: Tab) -> None:
        '''
        Switch to a specific tab.
        '''
        if tab.window_handle is not None and tab.manager is self and self.current_tab is not tab:
            self.current_tab = tab
            self.switch_to.window(self.current_tab.window_handle)

        else:
            print('Tab is either not part of this manager or is not open!')

    def execute_all_on_indicated(self, timeout=10) -> Dict[str, Any]:
        '''
        For all the currently open tabs, when the indicator element is present,
        or after waiting for a specified time (implicit_wait),
        run the tab's on_indicator_elem_found method and return the results. 
        '''
        ret: Dict[str, Any] = {}
        for tab in self.opened_tabs:
            if tab.indicator_element is not None:
                self.switch_to.window(tab.window_handle)
                try:
                    WebDriverWait(self, timeout).until(
                        EC.presence_of_element_located((tab.indicator_element[0], tab.indicator_element[1]))
                    )
                    ret[tab.name] = tab.on_indicator_elem_found()
                except TimeoutException:
                    ret[tab.name] = tab.on_indicator_elem_not_found()
            elif tab.implicit_wait is not None:
                self.switch_to.window(tab.window_handle)
                sleep(tab.implicit_wait * 1000)
                ret[tab.name] = tab.on_indicator_elem_found()
    
        return ret

if __name__ == '__main__':
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
    manager = ChromeTabManager(tabs=[tab1, tab2, tab3],
                           executable_path='./chromedriver',
                           desired_capabilities=caps,
                           options=opts)

    # Open all the tabs that were added on the manager's initialization
    manager.open_tabs()
    sleep(5)
    manager.quit()

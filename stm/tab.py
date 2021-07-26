from typing import Optional
from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Tab():
    def __init__(self,
                 name: str,
                 url: str,
                 indicatorElement: Optional[str] = None):

        self.name = name
        self.url = url
        self.indicatorElement = indicatorElement
        self.handleName: Optional[str] = None

    def setHandle(self, handleName: str):
        '''
        Assign the name of the handle that the webdriver uses for the tab.
        '''
        self.handleName = handleName
    
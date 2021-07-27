from typing import Optional

'''
Note: Cannot import manager.py for typing because of circular imports
'''

class Tab():
    def __init__(self,
                 name: str,
                 url: str,
                 indicatorElement: Optional[str] = None):

        self.name = name
        self.url = url
        self.indicatorElement = indicatorElement
        self.manager = None
        self.handleName: Optional[str] = None
        self.position: Optional[int] = None

    def setManager(self, manager):
        '''
        Assign a manager to the tab.
        '''
        self.manager = manager

    def setHandle(self, handleName: str):
        '''
        Assign the name of the handle that the webdriver uses for the tab.
        '''
        self.handleName = handleName
    
    def setPosition(self, position: int):
        '''
        Assign the index of the tab in the manager's tab list.
        '''
        self.position = position
    
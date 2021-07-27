# Note: Cannot import manager.py for typing because of circular imports
from typing import Optional

class Tab():
    def __init__(self,
                 name: str,
                 url: str,
                 indicator_element: Optional[str] = None):

        self.name = name
        self.url = url
        self.indicator_element = indicator_element
        self.manager = None
        self.handle_name: Optional[str] = None
        self.position: Optional[int] = None

    def set_manager(self, manager):
        '''
        Assign a manager to the tab.
        '''
        self.manager = manager

    def set_handle(self, handleName: str):
        '''
        Assign the name of the handle that the webdriver uses for the tab.
        '''
        self.handle_name = handleName
    
    def set_position(self, position: int):
        '''
        Assign the index of the tab in the manager's tab list.
        '''
        self.position = position
        
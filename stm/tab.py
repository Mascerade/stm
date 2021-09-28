from __future__ import annotations
from typing import Sequence, Optional, Union, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from stm.manager import ChromeTabManager

class Tab():
    '''
    Class that contains information for each tab opened.
    indicator_element: A tuple of the type of element to by found (By.ELEMENT_TYPE)
                       and the string for that property.
    '''
    def __init__(self,
                 name: str,
                 url: str,
                 indicator_element: Optional[Sequence[Union[Any, str]]] = None):

        self.name = name
        self.url = url
        self.indicator_element = indicator_element
        self.manager: Optional[ChromeTabManager] = None
        self.window_handle: Optional[str] = None
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
        self.window_handle = handleName
    
    def set_position(self, position: int):
        '''
        Assign the index of the tab in the manager's tab list.
        '''
        self.position = position
    
    def on_indicator_elem_found(self) -> Any:
        '''
        Function that executes once the indicator element is found.
        Only applies if you are using execute_all_on_indicated.
        Default functionality is to simply return the page_source.
        '''
        if self.manager is not None:
            return self.manager.page_source
        else:
            return None
    
    def on_indicator_elem_not_found(self) -> Any:
        '''
        Function that executes if the indicator element is not found.
        Onlyt applies if you are using execute_all_on_indicated
        Default functionality is to simply return the page_source.
        '''
        if self.manager is not None:
            return self.manager.page_source
        else:
            return None
    
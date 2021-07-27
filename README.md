# stm
<b>S</b>elenium <b>T</b>ab <b>M</b>anager is a wrapper around a driver that allows for easier management of tabs using Selenium.

## Example:
```python
# Create the tabs to use and create the manager
amazon = Tab('Amazon', 'https://www.amazon.com/', indicator_element=(By.ID, 'navbar'))
google = Tab('Google', 'https://www.google.com/', indicator_element=(By.ID, 'hpctaplay'))
apple = Tab('Apple', 'https://www.apple.com/', indicator_element=(By.ID, 'ac-globalnav'))
manager = ChromeTabManager(tabs=[amazon, google, apple],
                        executable_path='./chromedriver',
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
```

## Output:
```python
Amazon <html lang="en-us" class=" a-js a-audio a-video a-canvas a-svg a-drag-drop a-geolocation a-history a
________________________________
Google <html itemscope="" itemtype="http://schema.org/WebPage" lang="en"><head><meta charset="UTF-8"><meta 
________________________________
Apple <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en-US" lang="en-US" prefix="og: http://ogp.me/n
________________________________

```

This example illustrates how you can easily open new tabs and run functions on them. Here, we wait for specific elements to be loaded for each page and once they are loaded, we return the page source for that particular page.

`stm` is a wrapper around a regular Chrome webdriver, so if we want to do something for a tab using vanilla Selenium, we can:

```python
manager.switch_to_tab_by_obj(amazon)
elem = manager.find_elements_by_class_name("content")
print(elem.text)
```
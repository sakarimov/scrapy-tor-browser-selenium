# Scrapy with Tor-Browser-Selenium

### Pay attention to the [#Installation](https://github.com/sakarimov/scrapy-tor-browser-selenium?tab=readme-ov-file#installation) and the [#Configuration](https://github.com/sakarimov/scrapy-tor-browser-selenium?tab=readme-ov-file#configuration) sections.

---
The Scrapy middleware to use [tor-browser-selenium](https://github.com/webfp/tor-browser-selenium)

## Installation
```
$ pip install git+https://github.com/sakarimov/scrapy-tor-browser-selenium
```
You should use **Python>=3.6**.
You will also need [tor](https://torproject.org) and [tor-browser-selenium](https://github.com/webfp/tor-browser-selenium)

## Configuration
1. for this to run you have to specify the path to the tor-browser executable
```python
TBS_BROWSER_EXECUTABLE_PATH = "/path/to/tor-browser"
```
by default it will run tor-browser in headless mode, but you can change it by adding this to scrapy settings
```python
TBS_BROWSER_HEADLESS = False
```

2. Add the `addon` to the ADDON:
```python
ADDON = {
    "scrapytbs.tbsAddon": 543
}
```

## Usage
Use the `scrapytbs.tbsRequest` instead of the Scrapy built-in `Request` like below:
```python
from scrapytbs import tbsRequest

yield tbsRequest(url=url, callback=self.parse_result)
```
The request will be handled by tor-browser-selenium, and the request will have an additional `meta` key, named `driver` containing the Selenium driver with the request processed.
```python
def parse_result(self, response):
    print(response.request.meta["driver"].title)
```
For more information about the available driver methods and attributes, refer to the [tor-browser-selenium](https://github.com/webfp/tor-browser-selenium) or [Selenium with Python documentation](https://selenium-python.readthedocs.io/api.html#webdriver-api).

The `selector` response attribute works as usual (but contains the HTML processed by the Selenium driver).
```python
def parse_result(self, response):
    print(response.selector.xpath("//title/@text"))
```

### Additional arguments
The `scrapytbs.tbsRequest` accepts 4 additional arguments:

#### `wait_time`/`wait_until`

When used, Selenium will perform an [Explicit wait](http://selenium-python.readthedocs.io/waits.html#explicit-waits) before returning the response to the spider.
```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

yield tbsRequest(
    url=url,
    callback=self.parse_result,
    wait_time=10,
    wait_until=EC.element_to_be_clickable((By.ID, "someid"))
)
```

#### `screenshot`
When used, Selenium will take a screenshot of the page, and the binary data of the .png captured will be added to the response `meta`:
```python
yield tbsRequest(
    url=url,
    callback=self.parse_result,
    screenshot=True
)

def parse_result(self, response):
    with open("image.png", "wb") as image_file:
        image_file.write(response.meta["screenshot"])
```

#### `script`
When used, Selenium will execute custom JavaScript code.
```python
yield tbsRequest(
    url=url,
    callback=self.parse_result,
    script="window.scrollTo(0, document.body.scrollHeight);"
)
```

### TODO
- add ability to add Options() to the driver

# pybro

pybro is a python module that provide access to different browsers database.

## Getting Started

Currently, pybro supports *Firefox*, *Google Chrome* and *Chrominum*.

### Prerequisites

**Python 3** should be installed, or just [downlod](https://www.python.org) and install it.

### Installing

- Open command prompt

```shell
$ pip install pybro
```

Or :

```shell
$ git clone https://github.com/ahmed-BH/pybro.git
$ cd pybro
$ python setup.py install
```

### Examples

```python
>>> import pybro
>>> Browser.get_supported_br()
```
- Get a list of currently supported browsers

```python
>>> import pybro
>>> browser = pybro.Browser(name="firefox")
```
- Idicate which browser to use using **name** keyword
- if the entered browser is not valid or is unsupported yet, a *ValueError* exception will be raised.

```python
>>> key_words = browser.get_keyword_search(max=10)
>>> for i in key_words :
>>>    print(i)
```
- Provide **max** returned result or just don't provide max value to get all result.

```python
>>> downloads = browser.get_downloads(max=5)
>>> for i in downloads :
>>>    print(i["filename"])
```
- **get_downloads** method returns a list of *dicts*, its keywords are :

* file_name  
* file_type
* file_size
* site_url
* full_url
* start_time
* state
* received_bytes 
* danger

```python
>>> visits = browser.get_visited_ws(max=5)
>>> for i in visits :
>>>    print(i["url"])
```
- **get_visited_ws()** method returns a list of *dicts* sorted by *nb_visits*, its keywords are :

* url
* last_visit_time
* nb_visits


```python
>>> bmarks = browser.get_bookmarks(max=7)
>>> for i in bmarks :
>>>    print(i["title"])
```
- **get_bookmarks()** method returns a list of *dicts* sorted by *nb_visits*, its keywords are :

* url
* title

```python
>>> fill = browser.get_autoFill(max=7)
>>> for i in fill :
>>>    print(i["value"])
```
- **get_autoFill()** method returns a list of *dicts* sorted by *nb_visits*, its keywords are :

* value
* date_last_used

### Forensics

|  | Firefox | Chrome/Chromium |
|---------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Linux | ~/.mozilla/firefox/<profile> | ~/.config/google-chrome ~/.config/google-chrome-beta ~/.config/google-chrome-unstable ~/.config/chromium |
| Mac OS | ~/Library/Mozilla/Firefox/Profiles/<profile> ~/Library/Application Support/Firefox/Profiles/<profile> | ~/Library/Application Support/Google/Chrome ~/Library/Application Support/Chromium ~/Library/Application Support/Google/Chrome Canary |
| Windows | %AppData%/Mozilla/Firefox/Profiles/<profile> | %LOCALAPPDATA%\Google\Chrome\User Data\ChromeDefaultData %LOCALAPPDATA%\Chromium\UserData %LOCALAPPDATA%\Google\Chrome SxS\UserData |

### To Do List 

- [ ] Support Opera browser
- [ ] Support Safari browser
- [ ] Support Microsoft Edge :fearful:
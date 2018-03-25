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

---

### Forensics

<table>
  <tbody>
    <tr>
      <th></th>
      <th align="center">Firefox</th>
      <th align="center">Chrome/Chromium</th>
    </tr>
    <tr>
      <td>Linux</td>
      <td align="center">
      	<ul>
      		<li>~/.mozilla/firefox/<profileID>/places.sqlite</li>
      	</ul>
      </td>
      <td align="center">
      	<ul>
      		<li>~/.config/google-chrome/History</li>
      		<li>~/.config/google-chrome-beta/History</li>
      		<li>~/.config/google-chrome-unstable/History</li>
      		<li>~/.config/chromium/History</li>
      	</ul>

      </td>
    </tr>
    <tr>
      <td>Mac OS</td>
      <td align="center">
      	<ul>
      		<li>~/Library/Mozilla/Firefox/Profiles/<profileID>/places.sqlite</li>
      		<li>~/Library/Application Support/Firefox/Profiles/<profileID>/places.sqlite</li>
      	</ul>
      </td>
      <td align="center">
      	<ul>
      		<li>~/Library/Application Support/Google/Chrome/History</li>
      		<li>~/Library/Application Support/Chromium/History</li>
      		<li>~/Library/Application Support/Google/Chrome Canary/History</li>
      	</ul>
      </td>
    </tr>
    <tr>
      <td>Windows</td>
      <td align="center">
      	<ul>
      		<li>%AppData%/Mozilla/Firefox/Profiles/<profileID>/places.sqlite</li>
      	</ul>
      </td>
      <td align="center">
      	<ul>
      		<li>%LOCALAPPDATA%\Google\Chrome\User Data\ChromeDefaultData\History</li>
      		<li>%LOCALAPPDATA%\Chromium\UserData\History</li>
      		<li>%LOCALAPPDATA%\Google\Chrome SxS\UserData\History</li>
      	</ul>
      </td>
    </tr>
  </tbody>
</table>

### To Do List 

- [ ] Support Opera browser
- [ ] Support Safari browser
- [ ] Support Microsoft Edge :fearful:
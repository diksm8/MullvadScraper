#MullvadScraper
Scraper made in python to find accounts on mullvad.net.
The auth method can also be used for other csrf protected websites.

##Disclaimer
If you run too many threads at once they will start to time out and the program will crash, burn and break. Please refrain from being an idiot since I am too much of one to fix this problem. You need to kill the python process if this happens.

##ToDo
- [X] Threading
- [X] 12 random digits checker
- [X] Read accounts from list and check
- [X] Exception handling
- [X] Make the fileChecker script part of mullvad.py as a second click command
- [ ] Click progressbar
- [ ] Save to file using click
- [ ] Continue from last number
- [ ] Keyboard interrupt to close
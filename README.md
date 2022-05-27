# rightmove-webscraper

This repository provides a small extension to: https://github.com/toby-p/rightmove_webscraper.py

http://www.rightmove.co.uk/ is one of the UK's largest property listings websites, hosting thousands of listings of properties for sale and to rent.

rightmove_webscraper.py is a simple Python interface to scrape property listings from the website and prepare them in a Pandas dataframe for analysis.

new_property_scrapper.py is a simple script that sends email if a new property listing is published on the website for a set of filters. 

## Installation

Cd to `rightmove_webscraper` folder and run `pip install -r requirements.txt`

new_property_scrapper.py probably only works with Microsot Outlook installed

## How to use

Cd to `rightmove_webscraper` folder and 

1) specify search criteria and email address in the `config.json` file

2) run `new_property_scrapper.py`

The program will check every 5 minutes if a new property was updated on the website. 

In the standard settings the scrapper is only looking for properties in Glasgow. If one wants to search in another area

1) Go to "http://www.rightmove.co.uk/" and search for whatever listings you are interested in ...

2) Filter the search however you choose ...

3) Run the search and copy the URL of the results page ...

4) Paste the first part of the link into `new_property_scrapper.py` as the variable `PREFIX` (e.g. "https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION%5E61466&") and specify the other filters in the 
 `config.json` 

Legal

@pauldrm has pointed out per the terms and conditions here the use of webscrapers is unauthorised by rightmove. So please don't use this package!

**Mapofplay Spider**

a scrapy spider to get data from mapofplay.kaboom.org. it collects information about play grounds in all cities.
it returns a json file (or csv file) including 

-playground name

-playground address

-playground longitude

-playground latitude 

**How to run it**

from the command line

-cd mapofplay_scrapper

-pip install -r requirements.txt

-cd mapofplay_spider

-scrapy crawl mapofplay -o results.json

it will take a few hours to collect all the data.
# time-crawler
## To test the crawler for yourself, follow the steps listed below.
1. Install Scrapy using the following command:
```
pip install scrapy
```
2. Create a ```time-crawler``` directory and begin a new Scrapy project by running the following command in the ```time-crawler``` directory:
```
scrapy startproject time
```
This will create a ```time``` directory with the following contents:
```
time/
    scrapy.cfg
    time/
        __init__.py
        items.py
        middlewares.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
```
3. In the ```spiders``` directory, create a file named ```time_spider.py```, in which you will place the code from this repository.

4. To release the crawler and redirect its output into a file named ```time.json```, run the following command in the ```spiders``` directory:
```
scrapy crawl time -o time.json
```
Now, ```time.json``` should contain about 13,000 dictionaries, each storing a unique article's link, title, author, date, and body.

## To upload the contents of ```time.json``` to a public Elasticsearch domain, follow the steps listed below.
1. Since the dictionaries in ```time.json``` are contained within a single array, delete the first and last lines of the file. The only characters to be deleted should be ```[``` and ```]```.

2. To remove the commas from the end of each line, run the following command:
```
sed 's/,$//' < time.json > time1.json
```
This will create a new file named ```time1.json```.

3. To follow the format required by Elasticsearch, insert ```{"index": {"_index": "stories"}}``` before each dictionary by running the following command:
```
sed 's/^/{"index": {"_index": "stories"}}\n/g' < time1.json > time2.json
```
This will create a new file named ```time2.json```.

4. To upload the contents of ```time2.json``` to your cluster, run the following command, replacing ```ENDPOINT``` with your domain's endpoint:
```
curl -XPOST ENDPOINT/_bulk --data-binary @time2.json -H 'Content-Type: application/json'
```
NOTE: Due to its size, you may not be able to upload all of ```time2.json``` at once, requiring you to split it into multiple files, which must be uploaded individually. Splitting the file can be done using the following command, in which ```COUNT``` is an integer representing the number of lines in each new file, and ```PREFIX``` is a string representing the prefix of each new file's name:
```
split -l COUNT time2.json PREFIX
```

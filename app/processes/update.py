from processes.url_scrape import URLScrape, root_links
from processes.scrape import Scrape


import django
django.setup()

# Get staff_urls
print("Getting staff URLs")
urls = URLScrape(root_links)

# Scrape staff profile and add to dB
print("Getting staff profiles and updating database")
for i, url in enumerate(urls.all_staff):

    print("{}/{}".format(i, len(urls.all_staff)), url)
    item = Scrape(url=url, add_to_db=True)
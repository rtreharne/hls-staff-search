
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from itertools import chain


# These are the urls for all directives in HLS
root_links = [
              "https://www.liverpool.ac.uk/life-course-and-medical-sciences/",
              "https://www.liverpool.ac.uk/population-health/",
              "https://www.liverpool.ac.uk/infection-veterinary-and-ecological-sciences/",
              "https://www.liverpool.ac.uk/systems-molecular-and-integrative-biology/staff/",
              "https://www.liverpool.ac.uk/systems-molecular-and-integrative-biology/staff/life-sciences/",
               "https://www.liverpool.ac.uk/systems-molecular-and-integrative-biology/staff/biochemistry-and-systems-biology/",
               "https://www.liverpool.ac.uk/systems-molecular-and-integrative-biology/staff/molecular-and-clinical-cancer-medicine/",
               "https://www.liverpool.ac.uk/clinical-directorate/"
              ]

class URLScrape:
    def __init__(self, root_links):
        self.root_links = root_links
        self.staff = []

        for root in self.root_links:
            print(root)
            self.staff.append(self.get_staff_spider(root))

        self.all_staff = list(chain.from_iterable(self.staff))

    def get_soup_from_url(self, url):
        req = Request(url)
        html_page = urlopen(req)
        return BeautifulSoup(html_page, "lxml")

    def get_links_from_soup(self, soup):
        new_links = []
        links = [x.get('href') for x in soup.findAll('a') if x.get('href')]
        return links

    def get_links_from_url(self, url, domain="https://liverpool.ac.uk"):
        try:
            links = self.get_links_from_soup(self.get_soup_from_url(url))
        except ValueError:
            links = self.get_links_from_soup(self.get_soup_from_url(domain + url))
        return links

    def get_staff_urls(self, root):
        print("Get_staff_urls", root)
        urls = [x for x in self.get_links_from_url(root) if "/staff/" in x]
        return urls

    def get_staff_spider(self, root, save=[]):
        staff_urls = self.get_staff_urls(root)

        for url in staff_urls:

            if url not in save:

                save.append(url)

                if len(url.split("/staff/")[-1].split("-")) != 2:
                    try:
                        self.get_staff_spider(url, save=save)
                    except:
                        continue

        return save

urls = URLScrape(root_links)
for x in urls.all_staff:
    print(x)




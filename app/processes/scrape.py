
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from datetime import datetime
from django.utils.timezone import make_aware
from staff.models import Profile, Department
from django.conf import settings
from pathlib import Path

# Setup config for log file
log_string = "testing log"
log_fname = str(Path(settings.BASE_DIR)) + "/" + "profile_log.txt"

test_url = "https://www.liverpool.ac.uk/systems-molecular-and-integrative-biology/staff/robert-treharne/"



class Scrape:

    def __init__(self, url, add_to_db=False):
        self.url = url
        self.soup = self.get_soup_from_url(self.url)
        self.isstaff = self.check_if_staff()



        if self.isstaff:
            self.first_name, self.last_name = self.get_name_from_name_role()
            self.role = self.get_role()
            self.department = self.get_department()
            self.email = self.get_email()

            self.last_updated = self.get_last_updated()
            self.data = self.get_profile_info()

            self.profile = {"last_name": self.last_name,
                            "first_name": self.first_name,
                            "role": self.role,
                            # not updating department at the moment
                            "email": self.email,
                            "last_updated": self.last_updated}

            self.profile.update(self.data)

            if self.email != "":
                if add_to_db:
                    self.create_update()


    def create_update(self):
        # check for existing record


        try:
            record = Profile.objects.get(email=self.email)
        except:
            record = False

        if record:
            print("printing record: ", record)
            update_string = ""

            for key in self.profile:
                if record.__dict__[key] != self.profile[key]:
                    update_string += key + ", "
                    record.__dict__["last_updated"] = make_aware(datetime.now())
                    record.__dict__[key] = self.profile[key]

            if update_string != "":
                record.save()
                log_string = "{0}: The fields: {1} were updated on {2}'s profile\n".format(make_aware(datetime.now()), update_string[:-1], self.profile["last_name"] + " " + self.profile["first_name"])
                with open(log_fname, "a") as f:
                    f.write(log_string)
            else:
                print("no update for {}".format(self.profile["last_name"] + " " + self.profile["first_name"]))

            return record

        else:
            print("Creating new staff profile")
            new_staff = Profile(
                first_name = self.first_name,
                last_name = self.last_name,
                role = self.role,
                email = self.email,
                url = self.url,
                department = self.add_department(),
                last_updated = self.last_updated,
                about = self.data["about"],
                research = self.data["research"],
                publications = self.data["publications"],
                teaching = self.data["teaching"],
                professional_activities = self.data["professional_activities"]
            )
            #if "ZZ (DO NOT USE)" not in new_staff.department.name:
            new_staff.save()

    def add_department(self):
        try:
            department = Department.objects.get(name=self.department)
            return department
        except:
            new_department = Department(name=self.department)
            new_department.save()
            return new_department

    def get_soup_from_url(self, url):
        try:
            req = Request(url)
            html_page = urlopen(req)
            return BeautifulSoup(html_page, "lxml")
        except:
            return None

    def check_if_staff(self):
        try:
            name_role = self.soup.find("div", {"id": "name-role"})
            return name_role
        except:
            return None

    def get_name_from_name_role(self):

        family_name = self.isstaff.find("span", {"class": "family-name"}).text
        first_name = self.isstaff.find("span", {"class": "given-name"}).text
        return first_name, family_name

    def get_role(self):
        role = self.isstaff.find("span", {"class": "role"}).text
        return role

    def get_department(self):
        department = self.isstaff.find("span", {"class": "org"}).text
        return department

    def get_email(self):
        phone_email_web = self.soup.find("div", {"id": "phone-email-web"})
        email_block = phone_email_web.find("li", {"class": "email"})
        try:
            email = [x for x in email_block.find_all('a', href=True)][0].text
        except:
            email = ""
        return email

    def get_last_updated(self):
        last_updated = self.soup.find("meta", {"name": "Last updated"}).attrs["content"]
        date = datetime.strptime(last_updated, "%a, %b %d, %Y")
        return make_aware(date)

    def get_profile_info(self):
        url_map = {
            "about": {"url_suffix": "", "search": ["article", {"id": "staff-profile"}]},
            "research": {"url_suffix": "research", "search": ["div", {"class": "research-information"}]},
            "publications": {"url_suffix": "publications", "search": ["div", {"class": "publications-information"}]},
            "teaching": {"url_suffix": "teaching-and-learning",
                         "search": ["div", {"class": "teaching-and-learning-information"}]},
            "professional_activities": {"url_suffix": "external-engagement",
                                        "search": ["div", {"class": "external-engagement-information"}]},
        }

        data = {}

        for key in url_map:
            try:
                url = self.append_slash(self.url)
                page = self.get_soup_from_url(url + url_map[key]["url_suffix"])
                tag, tag_marks = url_map[key]["search"]

                t = page.find(tag, tag_marks).text
                data[key] = t
            except:
                data[key] = None
        return data

    def append_slash(self, url):
        if str(url)[-1] != "/":
            return url + "/"
        else:
            return url


print("Scraping")
Scrape(test_url, add_to_db=True)

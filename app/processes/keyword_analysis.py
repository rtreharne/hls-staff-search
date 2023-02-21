# Objective: Find how many times a keyword occurs across all profiles
# Only count matches from single profile as single occurence

import django
django.setup()

from staff.models import Profile, Keyword

keywords = Keyword.objects.all()
profiles = Profile.objects.all()

for keyword in keywords[:]:

    count = 0
    for profile in profiles:
        data = str(profile.about) + str(profile.research) + str(profile.teaching) + str(profile.publications) + str(profile.professional_activities)
        if keyword.keyword in data:
            count += 1
    keyword.frequency = count
    keyword.save()
    if count > 0:
        print(keyword.keyword, count)
import yake
from staff.models import Profile
import django
import time
django.setup()

start = time.time()
kw_extractor = yake.KeywordExtractor()

# get all profiles

profiles = Profile.objects.filter(visible=True)

text = ""

def xstr(s):
    if s is None:
        return ''
    return str(s)

print("Collating profiles ...")
for profile in profiles:
    profile_text = xstr(profile.about) + xstr(profile.research) + xstr(profile.publications) + xstr(profile.professional_activities)
    text += profile_text.lower()
print("... done.")

language = "en"
max_ngram_size = 2
deduplication_threshold = 0.2
num_of_keywords = 1000
print("Extracting keywords ...")
custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=num_of_keywords, features=None)
keywords = custom_kw_extractor.extract_keywords(text)


sorted_by_second = sorted(keywords, key=lambda tup: tup[1])[::-1]
for kw in sorted_by_second:
    print(kw)
print("Done")
end = time.time()
print("It took {} to extract keywords from {} profiles".format(end-start, len(profiles)))

from staff.models import Keyword

Keyword.objects.all().delete()
for kw in sorted_by_second:
    try:
        Keyword.objects.get(keyword=kw[0].lower())
    except:
        new_keyword = Keyword(keyword=kw[0].lower(),
                              score=kw[1])
        new_keyword.save()
    print(kw)
print("Done")
end = time.time()
print("It took {} to extract keywords from {} profiles".format(end-start, len(profiles)))



import django
django.setup()

from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from staff.models import Profile

vector = SearchVector("last_name",
                      "about",
                      "research",
                      "teaching",
                      "publications",
                      "professional_activities",
                      "additional_info")
query = SearchQuery("DASC508")

search = Profile.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.01).order_by('last_name').order_by('-rank')
print("done")

for item in search:
    print(item.last_name, item.rank)
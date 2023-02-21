from django.contrib import admin
from .models import Profile, Institute, Department, Directorate, Keyword, Banner
from django.utils.html import format_html


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'profile', 'department', 'visible')
    list_filter = ('department',)
    list_editable = ('visible', )
    search_fields = ('last_name', 'first_name', 'department__name')

    def profile(self, obj):
        return format_html("<a href='{url}', target='_blank'>Click for profile</a>", url=obj.url)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'institute')

    #def institute(self, obj):
        #return obj.institute.name
    list_editable = ('institute',)
    search_fields = ('name', 'institute__name',)

class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'score', 'frequency', 'visible')
    list_editable = ('visible',)
    search_fields = ('keyword',)





admin.site.register(Profile, ProfileAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Institute)
admin.site.register(Keyword, KeywordAdmin)
admin.site.register(Banner)

from features.models import University
from django.contrib import admin

class UniversityAdmin(admin.ModelAdmin):
	list_display = ('name', 'city', 'state')
	search_fields = ['name', 'city']

admin.site.register(University, UniversityAdmin)

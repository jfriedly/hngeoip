from django.db import models
from django.contrib.localflavor.us.models import USStateField

class University(models.Model):
	name = models.CharField(max_length = 128)
	city = models.CharField(max_length = 128)
	state = USStateField()
	
	def api_univ_name(self):
		return self.name.replace(' ','-')
	
	def api_city_name(self):
		return self.city.replace(' ','-')
	
	class Meta:
		verbose_name = "University"
		verbose_name_plural = "Universities"

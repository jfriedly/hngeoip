from django.http import HttpResponse, HttpRequest
from django.template import Context, loader
from features.models import University
from BeautifulSoup import BeautifulSoup
import pygeoip
import urllib2
import json

def index(request):
	client_address = request.META['REMOTE_ADDR']
	gi = pygeoip.GeoIP('/home/joel/dev/hngeoip/GeoLiteCity.dat')
	client_info = gi.record_by_addr(client_address)  # might need to add a str() here

	univ = University.objects.filter(city=client_info['city'], state=client_info['region_name'])
	if repr(type(univ)) == "<class 'features.models.University'>":
		nearby_univs = set(univ)
		print 1
	elif repr(type(univ)) == "<class 'django.db.models.query.QuerySet'>":
		nearby_univs = univ
		print 2, type(nearby_univs)
	else:
		raise MyError
		print 3
	
	queries = [client_info['metro_code'].replace(' ','-'), client_info['city'].replace(' ','-')]
	for uni in nearby_univs:
		queries.append(uni.name.replace(' ','-'))
	collections = ['users', 'items']
	addresses = {"users": [], "items": []}
	for x in collections:
		for y in queries:
			addresses[x].append("http://api.thriftdb.com/api.hnsearch.com/" + x + "/_search?q=" + y + "&pretty_print=true")
	print addresses
	searches = {"users": [], "items": []}
	for address in addresses["users"]:
		result = urllib2.urlopen(address).read()
		result_json = json.loads(result)
		searches["users"].append(result_json)
	for address in addresses["items"]:
		result = urllib2.urlopen(address).read()
		result_json = json.loads(result)
		searches["items"].append(result_json)
	print "hey, " + str(len(addresses))
	
	template = loader.get_template('features/index.html')
	context = Context({
		'client_address': client_address,
		'client_info': client_info,
		'nearby_univs': nearby_univs,
		'searches': searches,
	})
	return HttpResponse(template.render(context))

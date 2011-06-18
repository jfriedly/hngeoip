from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template import Context, loader
from features.models import University
import pygeoip
import urllib2
import json

def uniquify(some_list):
	checked = []
	for i in some_list:
		if i['item']['_id'] not in [x['item']['_id'] for x in checked]:
			checked.append(i)
	return checked


def load_no_location(client_address):
		template = loader.get_template('features/no-location.html')
		context = Context({
			'client_address': client_address,
		})
		print "Loading no location page"
		return HttpResponse(template.render(context))


def check_ip_database(value, client_info, client_address):
	piece = client_info.get(value, "")
	if piece == '':
		return load_no_location(client_address)



def index(request):
	client_address = request.META['REMOTE_ADDR']
	gi = pygeoip.GeoIP('/home/joel/dev/hngeoip/GeoLiteCity.dat')
	client_info = gi.record_by_addr(client_address) 

	no_city = check_ip_database('city', client_info, client_address)
	if no_city:
		return no_city
	no_region_name = check_ip_database('region_name', client_info, client_address)
	if no_region_name:
		return no_region_name
	no_metro_code = check_ip_database('metro_code', client_info, client_address)
	if no_metro_code:
		return no_metro_code

	nearby_univs = University.objects.filter(city=client_info['city'], state=client_info['region_name'])
	queries = [client_info['city'].replace(' ','-'), client_info['metro_code'].replace(' ','-')]
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
		search_result = urllib2.urlopen(address).read()
		result_json = json.loads(search_result)
		searches["users"].extend(result_json['results'])
	for address in addresses["items"]:
		search_result = urllib2.urlopen(address).read()
		result_json = json.loads(search_result)
		searches["items"].extend(result_json['results'])
	print "hey, " + str(len(addresses['users']) + len(addresses['items']))
	
	print "Joel, ", type(searches)
	print "is, ", type(searches["items"]), len(searches["items"])
	print "cool. ", searches['users'][0], type(searches["items"][0])
	
	searches['items'] = sorted(searches["items"], key=lambda x: x['score'])
	searches['users'] = sorted(searches["users"], key=lambda x: x['score'])
	searches['items'] = uniquify(searches['items'])
	searches['users'] = uniquify(searches['users'])

	queries = [query.replace('-',' ') for query in queries]
	template = loader.get_template('features/index.html')
	context = Context({
		'client_address': client_address,
		'client_info': client_info,
		'nearby_univs': nearby_univs,
		'searches': searches,
		'queries': queries,
	})
	return HttpResponse(template.render(context))



def eval(request):
	loc = request.POST['loc']
	city, region = loc.split(' ')
	if ',' in city:
		city = city.replace(',','')
	city = city.capitalize()
	state = region.upper()
	nearby_univs = University.objects.filter(city=city, state=state)
	queries = [city.replace(' ','-'), loc.replace(' ','-')]
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
		search_result = urllib2.urlopen(address).read()
		result_json = json.loads(search_result)
		searches["users"].extend(result_json['results'])
	for address in addresses["items"]:
		search_result = urllib2.urlopen(address).read()
		result_json = json.loads(search_result)
		searches["items"].extend(result_json['results'])
	print "hey, " + str(len(addresses['users']) + len(addresses['items']))
	
	print "Joel, ", type(searches)
	print "is, ", type(searches["items"]), len(searches["items"])
	print "cool. ", searches['users'][0], type(searches["items"][0])
	
	searches['items'] = sorted(searches["items"], key=lambda x: x['score'])
	searches['users'] = sorted(searches["users"], key=lambda x: x['score'])
	searches['items'] = uniquify(searches['items'])
	searches['users'] = uniquify(searches['users'])

	client_address = request.META['REMOTE_ADDR']
	client_info = {'city': city, 'region_name': state}
	queries = [query.replace('-',' ') for query in queries]
	template = loader.get_template('features/index.html')
	context = Context({
		'client_address': client_address,
		'client_info': client_info,
		'nearby_univs': nearby_univs,
		'searches': searches,
		'queries': queries,
	})
	#return HttpResponseRedirect('index.html')
	#return render_to_response(template, context, context_instance=RequestContext(request))
	return HttpResponse(template.render(context))

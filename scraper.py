import urllib2
from sys import argv, exc_info
from BeautifulSoup import BeautifulSoup

def get_args():
	"""Gets the string to search in the API and the collection to search."""
	collection = 'a'
	while (collection != 'i' and collection != 'items' and collection != 'item' and collection != 'u' and collection != 'users'  and collection != 'user'):
		try:
			script, collection, query = argv
		except (ValueError):
			print "Please enter the collection you would like to search followed by your query."
			collection = raw_input("Collection (items|users) >>> ")
			query = raw_input("Query                    >>> ") 
		if (collection != 'i' and collection != 'items' and collection != 'item' and collection != 'u' and collection != 'users'  and collection != 'user'):
			print "Please enter a valid value for collection."
	print collection 
	print query, type(query)
	return collection, query

def search(collection, query):
	"""Makes the request to the API and returns it."""
	if (collection == 'u' or collection == 'user'):
		collection = 'users'
	elif (collection == 'i' or collection == 'item'):
		collection = 'items'
	address = "http://api.thriftdb.com/api.hnsearch.com/" + collection + "/_search?q=" + query + "&pretty_print=true"
	print address + "\n"
	html = urllib2.urlopen(address).read()
	soup = BeautifulSoup(html)
	return soup


collection, query = get_args()
data = search(collection, query)
print data

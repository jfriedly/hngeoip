import csv
from features.models import University
from states import states

infile = open("/home/joel/Dropbox/issac-joel-shared/newest.csv")
reader = csv.DictReader(infile)

data = reader.next()

while data: 
	try:
	    univ, created = University.objects.get_or_create(
		    name = data['name'],
		    city = data['city'],
		    state = states.states[data['state']]
	    )
	except KeyError:
	    pass
	data = reader.next()


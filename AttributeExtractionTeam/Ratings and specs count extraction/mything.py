import json
import urllib
import json
import urllib
import copy as c
import numpy as np

def try_get(key, obj, no_complain=False):
	val = None

	try:
		val = obj[key]

	except KeyError as e:
		if not no_complain:
			print 'Warning: unsupported key: %s' %e

	except Exception as e:
		if not no_complain:
			print 'Warning: other exception: %s' %e

	return val

fnames = [something.json']
array={}
array1={}
all_products = []
copy =0
for fname in fnames:
	print '\treading %s' % fname
	full_fname =  fname
	all_products.extend(json.loads(open(full_fname, 'r').read()))
	

for prod in all_products:
	ratings = prod['ratings']
	if ratings is not None:
		for rating in ratings:
			#print rating['displayName']
			copy = rating['displayName']
			value = str(copy)
			if value in array:
				array[value] = array[value]+1
			else:
				array.update({value:1})

for prod in all_products:
	ratings = prod ['specs']
	if ratings is not None:
		for rating in ratings:
			#print rating['displayName']
			copy = rating['displayName']
			value = str(copy)
			if value in array1:
				array1[value] = array1[value]+1
			else:
				array1.update({value:1})


print "\nRatings\n"

for key in array:
	print key, array[key]
print "\nSpecifications\n"
for key in array1:
	print key,array1[key]


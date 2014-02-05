import json
import urllib
import copy as c
import numpy as np

#def query_api(query_str, params={}):
#
#	params.update({'api_key': API_KEY})
#	param_str = '&'.join([key+'='+str(val) for key,val in params.items()])
#	# todo: does not handle lists of vals!
#
#	url = "http://api.consumerreports.org/v0.1/" + query_str + '?' + param_str
#	print 'url: %s' % url
#
#	try: 
#		response_text = urllib.urlopen(url)
#	except:
#		print 'problem requesting data'
#		return False
#	
#	try:
#		response = json.loads(response_text)
#	except:
#		print 'problem parsing reply'
#		print response_text
#		return False
#	
#	return response
		

def make_category_listing(root_category_list):
	aggregator = {
		'phonebook': {},
		'human_list': '',
		'tree': []
	}

	for cat in root_category_list:
		recurse_category(cat, aggregator, aggregator['tree'])

	return aggregator


def recurse_category(category, aggregator, tree_parent, parent=None,
	franchise=None, depth=0):

	# Get the id, and make a blank entry in the phonebook for this category
	this_id = try_get('id', category)
	write_cat = {}


	# Copy all the fields that consumer reports includes, but don't include
	# child categories here
	for key, val in category.items():
		if key != 'downLevel':
			write_cat[key] = c.deepcopy(val)

	# Fill in the entry details
	write_cat['franchise'] = write_cat['id'] if depth==0 else franchise
	write_cat['parent'] = parent
	write_cat['depth'] = depth
	write_cat['children'] = []

	# write this category into the accumulating data structures
	aggregator['phonebook'][this_id] = write_cat
	write_cat_for_tree = c.deepcopy(write_cat)
	tree_parent.append(write_cat_for_tree)
	aggregator['human_list'] += '\t'*depth + str(this_id) + ' : ' + write_cat['singularName'] + '\n'

	# Recurse on the category's children, if any
	downLevel = try_get('downLevel', category, no_complain=True)
	if downLevel:
		for cat_type_key, children in downLevel.items():
			for child_cat in children:

				# Make a link to the children while we're at it
				write_cat['children'].append(
					recurse_category(child_cat, aggregator,
						write_cat_for_tree['children'], write_cat['id'], 
						write_cat['franchise'], depth+1))

	# Add some spaces to make the human_list a bit more readable
	if len(write_cat['children']):
		aggregator['human_list'] += '\n'

	return write_cat['id']
		


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


def prune_category(cat_id, cat_list):
	del_count = 0
	cat = cat_list[cat_id]
	for child_id in cat['children']:
		del_count += prune_category(child_id, cat_list)


	del cat_list[cat_id]
	del_count += 1

	return del_count


def collect_product_properties(prod_list):
	properties = {}

	num_prods = len(prod_list)
	for prod in prod_list:
		get_product_properties(prod, properties)

	# Turn all the values sets into lists, so they can be jsonified
	for key, prop in properties.items():

		if len(prop['numeric_values']):
			prop['avg_num'] = np.mean(prop['numeric_values'])
			prop['std_num'] = np.std(prop['numeric_values'])

		if len(prop['len']):
			prop['avg_len'] = np.mean(prop['len'])
			prop['std_len'] = np.std(prop['len'])

		# only repont unique values
		#prop['unique_values'] = list(set(prop['values']))

		del prop['values']
		del prop['numeric_values']
		del prop['len']

		prop['penetration'] = sum(prop['type'].values())*100 / float(num_prods)

	return properties


def get_product_properties(obj, properties={}):

	for key, val in obj.items():
		if key not in properties:
			properties[key] = get_blank_property_counter()

		record = properties[key]
		_type, _len = get_type(val)

		if _type is 'str':

			if not _len:
				record['type']['empty_str'] += 1
				record['values'].append(val)
				# don't include in length calculation

			elif _len < 20:
				record['type']['string'] += 1
				record['len'].append(_len)
				record['values'].append(val)

			else:
				record['type']['string'] += 1
				record['len'].append(_len)

		elif _type is 'null':
			record['type'][_type] += 1
			record['values'].append(None)
			# don't include in length calculation

		elif _type is 'int' or _type is 'float':
			record['type'][_type] += 1
			record['numeric_values'].append(val)
			# don't include in length calculation

		else:
			record['type'][_type] += 1
			record['len'].append(_len)

		if _type is 'dict':
			recurse_obj = {}
			for recurse_key, recurse_val in val.items():
				recurse_obj[key + '.' + recurse_key] = c.deepcopy(recurse_val)

			get_product_properties(recurse_obj, properties)
	


def get_type(val):
	if isinstance(val, int):
		return ('int', val)
	elif isinstance(val, float):
		return ('float', val)
	if isinstance(val, basestring):
		return ('str', len(val.strip()))
	if isinstance(val, list):
		return ('list', len(val))
	if isinstance(val, dict):
		return ('dict', len(val))
	if val is None:
		return ('null', 0)
	else:
		raise Exception('unexpected type: %s' % str(type(val)))


def get_blank_property_counter():
	return {
		'type' : {
			'int': 0,
			'float': 0,
			'string': 0,
			'list': 0,
			'dict': 0,
			'null': 0,
			'empty_str': 0
		},
		'len' : [],
		'values' : [],
		'numeric_values' : [],
		'avg_len' : None,
		'std_len' : None,
		'avg_num' : None,
		'std_num' : None
	}

def count_products(flat_categories, product_list):
	count = 0
	count_rated = 0
	count_tested = 0

	# Initialize all counts to be zero
	for cat_id, cat in flat_categories.items():
		cat['count'] = 0
		cat['count_rated'] = 0
		cat['count_tested'] = 0

	for prod in product_list:

		cat_id = prod['category']['id']
		count += 1

		flat_categories[cat_id]['count'] += 1
		if prod['isTested']:
			flat_categories[cat_id]['count_tested'] += 1
			count_tested += 1

		if 'ratings' in prod and len(prod['ratings']):
			flat_categories[cat_id]['count_rated'] += 1
			count_rated += 1


	return {
		'count':count,
		'count_rated':count_rated,
		'count_tested':count_tested
	}


def roll_up_counts(flat_categories):
	count = 0
	count_rated = 0
	count_tested = 0
	# We will drill down from the top
	franchises = filter(lambda x: x['depth'] == 0, flat_categories.values())
	for franchise in franchises:
		add_c, add_cr, add_ct = recurse_roll_up_product_counts(
			franchise, flat_categories)
		count += add_c
		count_rated += add_cr
		count_tested += add_ct
	
	return {
		'count':count,
		'count_rated':count_rated,
		'count_tested':count_tested
	}

def get_prods_by_cat(cat_id, prods):
	match_prods = filter(lambda p: p['category']['id'] == cat_id, prods)
	return match_prods

def get_prods_by_cat_recursive(cat_id, cats, prods):
	match_prods = get_prods_by_cat(cat_id, prods)
	for child_id in cats[cat_id]['children']:
		match_prods.extend(get_prods_by_cat_recursive(child_id, cats, prods))
	
	return match_prods


def tally_attributes(cats, prods):
	'''makes a comprehensive list of all attributes found among all the products
	of leaf categories.  Input is a flattened phonebook of categories (to
	find leaf categories, and a listing of all products.'''

	# We will tally attributes over leaf categories.  First, get the leaf
	# categories
	leaf_cats = filter(lambda c: len(c['children'])==0, cats.values())

	for cat in leaf_cats:

		# Get all the products in that category
		cat_prods = get_prods_by_cat(cat['id'], prods)
		
		# Make a first pass, to discover all of the ratings and specs in that
		# leaf category
		cat_ratings = {}
		cat_specs = {}
		cat_count = 0
		cat_union = None
		for prod in cat_prods:
			cat_count += 1
			ratings_obj = {}
			ratings = try_get('ratings', prod, no_complain=True)
			if ratings is not None:
				for rating in ratings:
					rating_key = rating['attributeId']
					ratings_obj[rating_key] = {}
					ratings_obj[rating_key]['name'] = rating['displayName']
					ratings_obj[rating_key]['count'] = 0
					ratings_obj[rating_key]['values'] = set()
					ratings_obj[rating_key]['CR_fields'] = {}
					CR_fields = ratings_obj[rating_key]['CR_fields']
					CR_fields.update(rating)

			cat_ratings.update(ratings_obj)

			specs_obj = {}
			specs = try_get('specs', prod, no_complain=True)
			if specs is not None:
				for spec in specs:
					spec_key = spec['attributeId']
					specs_obj[spec_key] = {}
					specs_obj[spec_key]['name'] = spec['displayName']
					specs_obj[spec_key]['count'] = 0
					specs_obj[spec_key]['values'] = set()
					specs_obj[spec_key]['CR_fields'] = {}
					CR_fields = specs_obj[spec_key]['CR_fields']
					CR_fields.update(spec)

			cat_specs.update(specs_obj)

			if cat_union is None:
				cat_union = set(cat_ratings.keys() + cat_specs.keys())
			else:
				cat_union &= set(cat_ratings.keys() + cat_specs.keys())


		# Make a second pass, to count how many of each of the ratings and
		# specs exist 
		for prod in cat_prods:
			ratings = try_get('ratings', prod, no_complain=True)
			if ratings is not None:
				for rating in ratings:
					rating_key = rating['attributeId']
					cat_ratings[rating_key]['count'] += 1
					cat_ratings[rating_key]['values'].add(rating['value'])

			specs = try_get('specs', prod, no_complain=True)
			if specs is not None:
				for spec in specs:
					spec_key = spec['attributeId']
					cat_specs[spec_key]['count'] += 1
					cat_specs[spec_key]['values'].add(spec['value'])

		# Now do some post-processing.  Compute the penetration (%age of
		# products having a given rating type.  Compute averages, etc
		for rating in cat_ratings.values():
			rating['penetration'] = rating['count'] / float(cat_count)

			# convert values to a list so it can be jsonified
			rating['values'] = list(rating['values'])

		for spec in cat_specs.values():
			spec['penetration'] = spec['count'] / float(cat_count)

			# convert values to a list so it can be jsonified
			spec['values'] = list(spec['values'])

		cat['attributes'] = dict(cat_ratings.items() + cat_specs.items())
		if cat_union is None or not len(cat['attributes']):
			cat['jaccard'] = None
		else:
			cat['jaccard'] = len(cat_union) / float(len(cat['attributes']))
	
	return cats


def roll_up_attributes(cats):
	'''cats should be a flat listing of categories that thas been annotated
	with listings of the attributes, and counts of their occurrence, in the
	products contained in the categories.  I.e, cats should be the output
	of tally_attributes.
	This rolls counts up to higher categories.
	'''
	# We'll start at the level of franchises
	franchises = get_franchises(cats)

	for franch in franchises:
		recurse_roll_up_attributes(franch, cats)
	
	# convert attribute value sets into lists for jsonifying
	for cat in cats.values():
		for feat in cat['attributes'].values():
			feat['values'] = list(feat['values'])

	return cats
		

def recurse_roll_up_attributes(cat, cats):

	if len(cat['children']):
		# Merge counts from its children
		attributes = {}
		attributes_union = None
		for child_id in cat['children']:
			child_cat = cats[child_id]
			child_attributes = recurse_roll_up_attributes(child_cat, cats) 
			if attributes_union is None:
				attributes_union = set(child_attributes.keys())
			else:
				attributes_union &= set(child_attributes.keys())

			for attribute_id, attribute in child_attributes.items():
				if attribute_id not in attributes:
					attributes[attribute_id] = {}
					attributes[attribute_id]['count'] = 0
					attributes[attribute_id]['values'] = set()
					attributes[attribute_id]['name'] = attribute['name']
					attributes[attribute_id]['CR_fields'] = attribute['CR_fields']

				attributes[attribute_id]['count'] += attribute['count']
				attributes[attribute_id]['values'] |= attribute['values']

		# Do aggregation
		if len(attributes):
			cat['jaccard'] = len(attributes_union) / float(len(attributes))
		else:
			cat['jaccard'] = None

		for attribute in attributes.values():
			attribute['penetration'] = attribute['count'] / float(cat['count'])

		cat['attributes'] = attributes
		return attributes
	
	else:
		# serve up own cats
		# note, higher levels always expect the 'values' to be sets.
		# at the very end, we'll convert back to lists for json output
		for feat in cat['attributes'].values():
			feat['values'] = set(feat['values'])

		return cat['attributes']

def summarize_attributes(attribute_annotated_cats):
	for cat in attribute_annotated_cats.values():
		new_attributes = {}
		for attribute in cat['attributes'].values():
			new_attributes[attribute['name']] = attribute['penetration']

		if len(new_attributes):
			cat['average_penetration'] = sum(
				new_attributes.values()) / float(len(new_attributes))
		else:
			cat['average_penetration'] = None

		cat['attributes'] = new_attributes
	
	return attribute_annotated_cats
		
def make_tree(flat_cats):
	'''makes a tree-like structure out of flat category structure
	'''
	tree = {}

	franchises = get_franchises(flat_cats)
	for franchise in franchises:
		tree[franchise['singularName']] = recurse_make_tree(
			franchise, flat_cats)

	return tree


def recurse_make_tree(cat, cats):
	tree_cat = c.deepcopy(cat)

	new_children = {}

	for child_id in tree_cat['children']:
		child_cat = recurse_make_tree(cats[child_id], cats)
		new_children[child_cat['singularName']] = child_cat

	tree_cat['children'] = new_children
	return tree_cat



def eliminate_singletons(cats):

	# This will eliminate categories that have only a single subcategory
	# the single subcategory will be graphted in the place of the category
	for cat_id, cat in cats.items():
		if len(cat['children']) is 1:

			# this category is a singleton
			# we will grapht its only child in its place 
			cat['type'] = 'singleton'
			singleton_id = cat_id
			grapht_id = cat['children'][0]
			parent = cats[cat['parent']]

			# first, remove the singleton from its parent
			parent['children'] = filter(
					lambda c: c != singleton_id, parent['children'])

			# grapht the only child onto the singleton's parent's child list
			parent['children'].append(grapht_id)
			cats[grapht_id]['parent'] = parent['id']

		else: 
			cat['type'] = 'category'
	
	return cats

			
def coalesce_by_jaccard(cats, jaccard_threshhold):
	franchises = get_franchises(cats)
	for franch in franchises:
		recurse_coalesce_by_jaccard(franch['id'], cats, jaccard_threshhold)

def recurse_coalesce_by_jaccard(cat_id, cats, jaccard_threshhold):

	cat = cats[cat_id]
	cat['path_to_equivalence'] = None

	# The first time jaccard goes above 0.8, we have an equivalence class
	# if we reach a leaf before this happens, the leaf is an equivalence class
	if cat['jaccard'] > jaccard_threshhold or len(cat['children']) is 0:
		cat['type'] = 'equivalence_class'

		# Once an equivalence class is found, we don't recursively find
		# equivalence classes, but we do recursively mark its children
		# as type = 'sub_equivalence'.  We also record the ancestral path
		# that leads from the equivalence class to each of its children
		# since these sub_equivalent categorizations will be mapped to 
		# attributes
		for child_id in cat['children']:
			record_equivalence_class_membership(
				child_id, cats, path=[cat_id])

	else :
		for child_id in cat['children']:
			recurse_coalesce_by_jaccard(child_id, cats, jaccard_threshhold)


def record_equivalence_class_membership(cat_id, cats, path):
	cat = cats[cat_id]
	cat['path'] = path
	cat['type'] = 'sub_equivalence'

	for child_id in cat['children']:
		record_equivalence_class_membership(child_id, cats, path + [cat_id])


	
def strip_down_tree(subtree):
	for cat in subtree.values():
		for key in cat.keys():
			if key not in ['jaccard', 'children', 'type']:
				del cat[key]

		if len(cat['children']):
			strip_down_tree(cat['children'])


def strip_down_cats(cats):
	''' this function removes extraneous attributes from category listings
	which will obscure the important information in the case of inspecting
	category-wise attribute penetration.
	'''
	for cat in cats.values():
		for prop in cat.keys():
			if prop not in ['parent', 'depth', 'count', 'children', 
				'singularName', 'attributes', 'id', 'jaccard']:
				del cat[prop]
	
	return cats



def get_franchises(flat_categories):
	return filter(lambda x: x['depth']==0, flat_categories.values())


def drill_print(flat_categories):
	franchises = get_franchises(flat_categories)
	for franch in franchises:
		recurse_drill_print(franch, flat_categories)


def recurse_drill_print(cat, flat_categories):
	counts = (cat['count'], cat['count_rated'], cat['count_tested'])

	errors = (
		cat['count'] - cat['productsCount'], 
		cat['count_rated'] - cat['ratedProductsCount'],
		cat['count_tested'] - cat['testedProductsCount']
	)
	print '\t'*cat['depth']+cat['singularName'],counts, '\t' + str(errors)
	for child_id in cat['children']:
		child_cat = flat_categories[child_id]
		recurse_drill_print(child_cat, flat_categories)

	if len(cat['children']):
		print ''


def recurse_roll_up_product_counts(category, flat_categories):
	child_count = 0
	child_count_rated = 0
	child_count_tested = 0
	for child_id in category['children']:
		child_cat = flat_categories[child_id]
		add_c, add_cr, add_ct = recurse_roll_up_product_counts(
			child_cat, flat_categories)
		child_count += add_c
		child_count_rated += add_cr
		child_count_tested += add_ct
	
	if not len(category['children']):
		return (category['count'], category['count_rated'],
			category['count_tested'])

	else:
		category['count'] = child_count
		category['count_rated'] = child_count_rated
		category['count_tested'] = child_count_tested
		return (child_count, child_count_rated, child_count_tested)


def reset_counts(flat_categories):
	for cat_id, cat in flat_categories.items():
		cat['count'] = 0


def check_for_cycle(flat_categories):
	franchises = filter(lambda x: x['depth'] == 0, flat_categories.values())
	done = set([])
	for franchise in franchises:
		print 'starting new franchise: len(done) = %d' % len(done)
		recurse_check_for_cycle(franchise, flat_categories, done)
	
	return len(done)


def recurse_check_for_cycle(cat, flat_categories, done):

	for cat_id in cat['children']:
		child_cat = flat_categories[cat_id]
		recurse_check_for_cycle(child_cat, flat_categories, done)
	
	if cat['id'] in done:
		print 'XXX :', cat['id']
	else:
		done.add(cat['id'])
		print '---'





def read_all_products():
	fnames = [
		'product_food.json',
		'product_appliances.json',
		'product_health.json',
		'product_babiesKids.json',
		'product_homeGarden.json',
		'product_cars.json',
		'product_money.json',
		'product_electronicsComputers.json'
	]

	all_products = []
	for fname in fnames:
		print '\treading %s' % fname
		all_products.extend(json.loads(open(fname, 'r').read()))
	
	return all_products



def get_cat_name_recursive(cat_id, cats):
	cat = cats[cat_id]
	cat_name = cat['singularName']
	for child_id in cat['children']:
		cat_name += ' ' + get_cat_name_recursive(child_id, cats)

	return cat_name


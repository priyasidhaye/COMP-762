import survey as s
import codecs
import json as j
import re


if __name__ == "__main__":
	cats = j.loads(open('categories_flat.json').read())
	prods = s.read_all_products()
	extract_all_equivalence(cats, prods)


def extract_all_equivalence(cats, prods, write_folder):
	for franch in s.get_franchises(cats):
		name = franch['singularName'].split()[0]
		if not write_folder.endswith('/'):
			write_folder += '/'
		fname = name + '_eq_text.csv'
		franch_id = franch['id']
		filt_cats = dict(
			filter(lambda c: c[1]['franchise'] == franch_id, cats.items()))
		extract_equivalence(filt_cats, prods, fname, 
			write_folder=write_folder, headings_in_file=False)


#Build a list of rows that will be entries in the db
def extract_equivalence(cats, prods, fname, write_folder='', 
		headings_in_file=False):

	# By default, we'll index equivalence classes
	USE_FIELD_TYPE = 'equivalence_class'

	fh = codecs.open(write_folder + fname, 'w', 'utf-8')
	is_first = True

	# to strip characters that can interfere with csv format
	escape_regex = re.compile(r'\r|\n|"|,|', re.I)

	# For each equivalence class, aggregate text fields
	for cat_id, cat in cats.items():
		if cat['type'] == USE_FIELD_TYPE:
			matched_prods = s.get_prods_by_cat_recursive(cat_id, cats, prods)

			aggregator = {
				'id': [],
				'description' : [],
				'bottomLine': [],
				'displayName' : [],
				'review': [],
				'summary': [],
				'highs' : [],
				'lows' : []
			}

			seen_brands = set()
			brand = []

			seen_ratings = set()
			rating_descriptions = []
			rating_names = []

			seen_specs = set()
			spec_descriptions = []
			spec_names = []

			for prod in matched_prods:

				# Grab various non-burried text fields
				for key, val in aggregator.items():
					try_append(val, prod, key)

				# Go digging for more text:

				# Grab the brand
				if 'brand' in prod:

					# Don't include duplicates
					if prod['brand']['id'] in seen_brands:
						continue
					else:
						seen_brands.add(prod['brand']['id'])

					# Get the brand name
					if 'displayName' in prod['brand']:
						brand.append(prod['brand']['displayName'])

				# Grab rating descriptions
				if 'ratings' in prod:
					for rating in prod['ratings']:

						# Don't include duplicates
						if rating['attributeId'] in seen_ratings:
							continue
						else:
							seen_ratings.add(rating['attributeId'])

						# Get the displayName and description if not duplicate
						if 'displayName' in rating:
							rating_names.append(rating['displayName'])

						if 'description' in rating:
							rating_descriptions.append(rating['description'])

				if 'specs' in prod:
					for spec in prod['specs']:

						# Don't include duplicates
						if spec['attributeId'] in seen_specs:
							continue
						else:
							seen_specs.add(spec['attributeId'])

						# Get the displayName and description if not duplicate
						if 'displayName' in spec:
							spec_names.append(spec['displayName'])
						
						if 'description' in spec:
							spec_descriptions.append(spec['description'])

			aggregator.update({
				'brand':brand,
				'rating_descriptions': rating_descriptions,
				'rating_names': rating_names,
				'spec_descriptions': spec_descriptions,
				'spec_names': spec_names
			})

			# the 'id' field in the aggregator is so-named to match and find
			# the 'id' field of the products, but we need to rename to 
			# 'prod_ids' so it doesn't collide with the eq_class's own id field
			aggregator['prod_ids'] = aggregator['id']
			del aggregator['id']

			# flatten and escape all fields in the aggregator
			for key, val in aggregator.items():
				aggregator[key] = ' '.join(val)
				aggregator[key] = escape_regex.sub('', aggregator[key])

			# If this is the first line, write out headings
			if is_first:
				is_first = False
				headings_text = write_cols_noenq(
						['cr_id', 'image_url', 'name', 'all_names'] +
						[col[0] for col in sorted(aggregator.items())])

				if headings_in_file:
					fh.write(headings_text)

				else:
					fheadings = open(write_folder + 'headings.txt', 'w')
					fheadings.write(headings_text)
					fheadings.close()
				
			# try to get an image file
			image_url = 'images/no_image.png'
			if 'imageCanonical' in cat:
				image_url = cat['imageCanonical']

			# Write out the csv line
			fh.write(write_cols(
				[cat_id, image_url, cat['singularName'], 
					s.get_cat_name_recursive(cat_id, cats)] + 
				[col[1] for col in sorted(aggregator.items())]))

	fh.close()

def write_cols(lst):
	return '"' + '","'.join(lst) + '"\n'

def write_cols_noenq(lst):
	return ','.join(lst) + '"\n'


def try_append(lst, dct, key):
	if key in dct:
		lst.append(dct[key])


		
		

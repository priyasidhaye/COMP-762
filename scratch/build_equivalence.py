import survey as s
import json as j
import copy as c
import sys

def factor_categories():
	print 'load cats'
	cats = j.loads(open('categories.json','r').read())

	print 'make categories phonebook'
	aggregator = s.make_category_listing(cats)
	flat_cats = aggregator['phonebook']
	tree_cats = aggregator['tree']

	print 'load products'
	prods = s.read_all_products()

	print 'fix product counts'
	s.count_products(flat_cats, prods)
	s.roll_up_counts(flat_cats)

	print 'prune food, money, and baby stuff'
	s.prune_category('28985', flat_cats) # Babies and kids
	s.prune_category('33546', flat_cats) # Food
	s.prune_category('34458', flat_cats) # Money

	print 'tally features'
	flat_cats = s.tally_features(flat_cats, prods)

	print 'roll up features'
	flat_cats = s.roll_up_features(flat_cats)

	print 'summarize_features'
	flat_cats = s.summarize_features(flat_cats)

	print 'make tree'
	tree = s.make_tree(flat_cats)

	print 'eliminate singletons'
	tree, flat_cats = s.eliminate_singletons(tree, flat_cats)

	print 'coalesce by jaccard'
	tree, flat_cats = s.coalesce_by_jaccard(tree, flat_cats)

	print 'simplify tree'
	s.strip_down_tree(tree)

	return tree, flat_cats

if __name__ == '__main__':
	if len(sys.argv) > 1:
		flat_cats_fname = sys.argv[1]
	else:
		flat_cats_fname = 'categories_flat.json'

	if len(sys.argv) > 2:
		tree_cats_fname = sys.argv[2]
	else:
		tree_cats_fname = 'categories_tree.json'

	tree, flat_cats = factor_categories()

	fh = open(flat_cats_fname, 'w')
	fh.write(j.dumps(flat_cats, indent=3))
	fh.close()

	fh = open(tree_cats_fname, 'w')
	fh.write(j.dumps(tree, indent=3))
	fh.close()


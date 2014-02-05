import survey as s
import json as j
import copy as c
import sys

JACCARD_THRESHHOLD = 0.8
PRUNE_CATEGORIES = ['28985', '33546', '34485']
#			Babies and kids,  Food, 	Money



def factor_categories():
	print 'load cats'
	cats = j.loads(open('categories.json','r').read())

	print 'make categories phonebook'
	aggregator = s.make_category_listing(cats)
	cats = aggregator['phonebook']
	tree_cats = aggregator['tree']

	print 'load products'
	prods = s.read_all_products()

	print 'fix product counts'
	s.count_products(cats, prods)
	s.roll_up_counts(cats)

	print 'prune food, money, and baby stuff'
	s.prune_category('28985', cats)
	s.prune_category('33546', cats) 
	s.prune_category('34458', cats) 

	print 'tally attributes'
	cats = s.tally_attributes(cats, prods)

	print 'roll up attributes'
	cats = s.roll_up_attributes(cats)

	print 'summarize_attributes'
	cats = s.summarize_attributes(cats)

	print 'eliminate singletons'
	cats = s.eliminate_singletons(cats)

	print 'coalesce by jaccard'
	s.coalesce_by_jaccard(cats, JACCARD_THRESHHOLD)

	print 'make tree'
	tree = s.make_tree(cats)

	print 'simplify tree'
	tree = c.deepcopy(tree)
	s.strip_down_tree(tree)

	return tree, cats

if __name__ == '__main__':
	if len(sys.argv) > 1:
		flat_cats_fname = sys.argv[1]
	else:
		flat_cats_fname = 'categories_flat.json'

	if len(sys.argv) > 2:
		tree_cats_fname = sys.argv[2]
	else:
		tree_cats_fname = 'categories_tree.json'

	tree, cats = factor_categories()

	fh = open(flat_cats_fname, 'w')
	fh.write(j.dumps(cats, indent=3))
	fh.close()

	fh = open(tree_cats_fname, 'w')
	fh.write(j.dumps(tree, indent=3))
	fh.close()


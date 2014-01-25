### Using this script ###
Copy the dataset into the same folder as build\_equivalence.py and survey.py.
on the command line, run `python build_equivalence.py` 
This will create two files named `categories_flat.json` and 
`categories_tree.json`.

You may provide two optional arguments which will be used respectively as the 
output 
filename for the flat category file and category tree file.

### What this script does ###
Most importantly, the script identifies equivalence classes within the existing
category structure of the CR database.

It does several other things on the way:
- provides a flat format for the categories
- eliminates singletons
- fixes incorrect counts
- adds other useful annotations
- creates an easy-to-visualize copy of the categorise for human viewing

Each of these items is described in more detail below

#### Idenifying equivalence classes ####
The script looks at products belonging to each **leaf** category, and finds 
the union
of all the `attributes` (`specs` and `ratings`) accross the category.
It computes the Jaccard index for the `attributes`.  

Once this has been performed on the leaf categories, it ''bubbles up'' the
Jaccard index to higher categories.  This is done by looking at all the 
`attributes` supported in the children of a category of interest, and 
calculating
the Jaccard index for the support of `attributes` accross these children.  This
carries straight up to franchises.

The Jaccard index provides a sort of *uniformity* measure within each category.

The script then descends the tree, depth first, and, when it discovers a 
category having `jaccard` higher than 0.8 (default), it declares the category
to be an *equivalence class*.  This is recorded in the category's `type` 
property as `type : 'equivalence_class'`.  The threshold `jaccard` needed to
declare an equivalence class can be tuned using the `JACCARD_THRESHHOLD`,
global in build\_equivalence.py.

Categories below an equivalence class will not be marked as an equivalence
class, but will all be marked as `type: 'sub_equivalence'`. Categorisations
below the level of an equivalence class could be transformed into a `spec`.
These sub\_equivalence categories have a field called `path` which provides
a list (array) of the category ids that are seen in a traversal from their 
ancestral equivalence class to their immediate parent.

Probing many cases shows that the equivalence classes are sensically defined
in general, but are too conservative sometimes.  that is, some categories are
not coalesced into equivalence classes even though they probably should be.
More on this below under the **Needed extension** heading, and some other
examples near the bottom of [this wiki page](https://github.com/priyasidhaye/COMP-762/wiki/Attributes-and-%22Product-Equivalence-Classes%22)



### Flat format for categories  ###
To ease lookups, the categories\_flat.json file lists all categories by their
`id` in a flat dictionary.  The tree structure emerges by virtue of the 
`children` and `parent` fields in category entries.  `children` is an array of
`id` strings, and parent is a single `id` string.


### Eliminating singletons ###
The CR categories hierarchy have many categrories that have only a single
child category, often with the same name as the parent.  Aside from being
redundant, it interferes with calculating meaningful Jaccard indices for 
`attributes`.  The script removes these.  An example will show how.  Consider
this subtree in the categories tree:

	Appliance
	  |
	  `- Kitchen Appliance
	        |
	        `- Dishwasher
	              |
	              `- Dishwasher
						|
						+- Dishwasher drawers
						|
						`- Conventional dishwashers

The **first** instance of Dishwasher gets marked `type : 'singleton'`, its 
reference in Kitchen Appliance `children` is removed, while a reference is 
added to the **second** instance of Dishwasher.  The second instance of
Dishwasher's `parent` field gets updated to the `id` of Kitchen Applience,
keeping the tree structure in tact.  The entry for the **first** instance of
Dishwasher remains, but it is not reachable through traversal of the tree
structure:

	Appliance
	  |
	  `- Kitchen Appliance
	  	    |
	  	    `- Dishwasher
	  	  		|
	  	  		+- Dishwasher drawers
	  	  		|
	  	  		`- Conventional dishwashers


	        *
			|
	        `- Dishwasher (no ref leads here)
	
The dangling entry for Dishwasher is kept so that lookups for its `id` in the 
categories flat file will succeed, and its `type` could simply be checked.
Dangling singletons still have their `parent` field unchanged, so that it is 
always possible to know "where they came from".


### fixing incorrect counts ###
The counts offered in the original fields `productsCount`, 
`ratedProductsCount`, `testedProductsCount`, and `testedProductsOnlyCount` 
are incorrect in many cases.  Use `count`, `count_rated`, and `count_tested`
instead.


### Other useful annotations ###
- `attributes`: dictionary listing union of all the attributes found in 
   products inside the category.  Each attribute is indexed by its 
   `displayName` and the associated value is its penetration (fraction of 
   products supporting the attribute).
- `average_penetration`: the unweighted average penetration of all features.
   A way to measure uniformity as an alternative to `jaccard`
- `depth`: Depth in the hierarchy.  Franchises have `depth : 0`.

### Visualizing the categories and equivalence classes ###
The file categories\_tree.json is intended to be a more human readable way
to visualize the categories structure resulting in categories\_flat.json.
The hierarchy is nested rather than by reference, and most of the fields have
been removed to prevent cluttering.  Use a json visualizing software, or just 
[click here](http://shpow.com/reports2html?file=categories_tree.json) and when 
the page loads click `htmlify`. 

### Extensions needed ###
At the moment, the script only tries to turn categories that existed in the 
original CR database into equivalence classes.  It's clear that sometimes
a **part** of a category should be an equivalence class.  An example will help:

	Appliance
	  |
	  `- Kitchen Appliance
	  	    |
	  	    `- Cooktop & wall oven
	  	  		|
	  	  		+- Electric cooktop
	  	  		|
	  	  		+- Gas cooktop
	  	  		|
	  	  		`- Wall oven

In this case it would probably make sense for Electric cooktop and Gas cooktop
to form an equivalence class, while Wall oven is put in a separate 
equivalence class.  

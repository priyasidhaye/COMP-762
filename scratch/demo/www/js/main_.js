
// replace existing handle_keydown with this
function handle_keydown(e) {
	if(e.which == 13) {
		get_products_single();
	}
}

// Put this anywhere in the script
function get_products_single() {
	data = {'query': 'cell phone'}  // just an example. 

	$.ajax({
		'url' : 'php/get_eq_class_single.php',
		'type': 'POST',
		'data': data,
		'dataType': 'json',
		'success': function(data, textStatus, jqXHR) {
			put_products(data);
		},
		'error': function(jqXHR, status, err) {
			alert(err);
		}
	});
}


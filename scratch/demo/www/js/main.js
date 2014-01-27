window.onload = init;
function init() {
	$('input').on('keydown', handle_keydown);
	$('#search_btn').on('keydown', handle_keydown);
	$('#search_btn').on('click', handle_click);	
}

function handle_keydown(e) {
	if (is_advanced_search) {	
		if(e.which == 13) {
			get_products();
		}
	} else {
		if(e.which == 13) {
			get_products_single();
		}
	}
}

function handle_click() {
	if (is_advanced_search) {	
		get_products();
	} else {
		get_products_single();
	}
}

function get_data(data) {
	return function(index) {
		var elm = $(this);
		if(elm.val() != '') {
			text = elm.val();
			text = text.split(' ');
			text = '%' + text.join('%,%') + '%';
			data[elm.attr('name')] = text;
		}
	}
}
function get_products_single() {
	var query = $('#main_search_text').val();
	if (query == '') {
		return;
	} 
	query = query.split(' ');
	query = '%' + query.join('%,%') + '%';
	data = {'query': query};

	$.ajax({
		'url' : 'php/get_eq_class_single.php',
		'type': 'POST',
		'data': data,
		'dataType': 'json',
		'success': function(data, textStatus, jqXHR) {
			console.log(data);
			put_products(data);
		},
		'error': function(jqXHR, status, err) {
			alert(err);
		}
	});
}

function get_products() {
	data = {}
	$('input').each(get_data(data));

	$.ajax({
		'url' : 'php/get_eq_class.php',
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

function put_products(products) {
	var products_wrapper = $('#products_wrapper');
	products_wrapper.html('');

	// tell user what's happening
	var show_msg = $('#show_msg');
	if(products.length) {
		show_msg.html('Did you mean...');
		show_msg.css('display', 'block');
	} else {
		show_msg.html('Sorry, no matches...');
		show_msg.css('display', 'block');
	}

	for(var i=0; i<products.length; i++) {
		var new_div = $("<div class='suggest_eq_class'>"+products[i]['name']+"</div>");
		var img = $("<img class='suggest_img' src='" + products[i]['image_url'] + "' />");
		var clear_div = $("<div class='clear'></div>");
		var suggest_div = $("<div class='suggest_div'></div>");
		suggest_div.append(img);
		suggest_div.append(new_div);
		suggest_div.append(clear_div);
		suggest_div.on('click', arm_suggest_on_click(products[i]['prod_ids']));
		products_wrapper.append(suggest_div);
	}
}

function arm_suggest_on_click(prod_ids) {
	return function (e) {
		alert(prod_ids.split(' ').join(', '));
	};
}

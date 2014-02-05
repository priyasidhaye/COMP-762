<?php

	require_once $_SERVER['DOCUMENT_ROOT'] . '/common/php/db.php'; 

	# Get the variables that were posted or get'ed
	$posted_var_names = array(
		'id',
		'name',
		'desc',
		'source_id',
		'create_time',
		'update_time',
		'id'
	);
	

	$posted_vars = array();
	foreach($posted_var_names as $var_name) {
		$posted_vars[$var_name] = get_var($var_name);
	}

	foreach($posted_vars as $key => $val) {
		echo "$key : $val <br/>";
	}
?>


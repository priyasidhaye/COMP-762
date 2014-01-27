<?php
	require_once $_SERVER['DOCUMENT_ROOT'] . '/common/php/db.php'; 
	$TABLE_NAME = 'eq_classes';
	$DB_NAME = 'uedwardn_cr';

	# Get a connection to the database
	$conn = connect_db($DB_NAME);

	# These are the variables expected via POST
	$posted_var_names = array('cr_id', 'name', 'all_names', 'bottomLine', 'brand', 'description', 'displayName', 'highs', 'lows', 'rating_descriptions', 'rating_names', 'review', 'spec_descriptions', 'spec_names', 'summary');
	
	# Get the POST variables
	$posted_vars = get_vars($posted_var_names);

	$posted_vars = filter_non_null($posted_vars);
	
	# Make an sql insert statement
	$sql = get_custom_query($conn, $TABLE_NAME, $posted_vars, array('name', 'image_url', 'prod_ids'));

	# Insert into the db
	$result = mysqli_query($conn, $sql);
	if($err = mysqli_error($conn)) {
		echo '{"success":false, "error":"'.$sql.'"}';
	} else {
		echo result2json($result);
	}

	function get_custom_query($conn, $table_name, $vars, $col_names=NULL) {
		if(is_null($col_names)) {
			$cols_expression = '*';
		} else {
			$cols_expression = '`' . implode('`,`',$col_names) . '`';
		}
		$sql = "SELECT $cols_expression FROM $table_name WHERE";

		$first = TRUE;
		foreach($vars as $col_name => $val) {
			if($first) {
				$first = FALSE;
			} else {
				$sql .= ' AND';
			}
			if(is_array($val)) {
				$sql .= " (";
				$inner_first = TRUE;
				foreach($val as $v) {
					if($inner_first) {
						$inner_first = FALSE;
					} else {
						$sql .= " AND";
					}
					$sql .= " `$col_name` LIKE " . enquote_and_mysql_escape($conn, $v);
				}
				$sql .= ")";
			} else {
				$sql .= " `$col_name` LIKE " . enquote_and_mysql_escape($conn, $val);
			}
		}
		return $sql;

	}
?>


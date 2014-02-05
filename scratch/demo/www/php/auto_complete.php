<?php
	require_once $_SERVER['DOCUMENT_ROOT'] . '/common/php/db.php'; 
	$TABLE_NAME = 'eq_classes';
	$DB_NAME = 'uedwardn_cr';

	# Get a connection to the database
	$conn = connect_db($DB_NAME);

	# These are the variables expected via POST
	$query_cols = array('name');
	
	$query = get_var('query');

//	# Get the POST variables
//	$posted_vars = get_vars($posted_var_names);
//
//	$posted_vars = filter_non_null($posted_vars);
	
	# Make an sql insert statement
	$sql = get_custom_query($conn, $TABLE_NAME, $query, $query_cols, array('name'));

	# Insert into the db
	$result = mysqli_query($conn, $sql);
	if($err = mysqli_error($conn)) {
		echo '{"success":false, "error":"'.$sql.'"}';
	} else {
		echo result2json($result);
	}

	function get_custom_query($conn, $table_name, $query, $query_cols, $get_col_names=NULL) {
		if(is_null($get_col_names)) {
			$cols_expression = '*';
		} else {
			$cols_expression = '`' . implode('`,`',$get_col_names) . '`';
		}
		$sql = "SELECT $cols_expression FROM $table_name WHERE";

		$first = TRUE;
		foreach($query_cols as $col_name) {
			if($first) {
				$first = FALSE;
			} else {
				$sql .= ' OR';
			}
			if(is_array($query)) {
				$sql .= " (";
				$inner_first = TRUE;
				foreach($query as $v) {
					if($inner_first) {
						$inner_first = FALSE;
					} else {
						$sql .= " AND";
					}
					$sql .= " `$col_name` LIKE " . enquote_and_mysql_escape($conn, $v);
				}
				$sql .= ")";
			} else {
				$sql .= " `$col_name` LIKE " . enquote_and_mysql_escape($conn, $query);
			}
		}
		return $sql;

	}
?>


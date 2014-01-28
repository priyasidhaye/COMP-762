<!DOCTYPE html>
<html>
	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
		<title>Product Exploration</title>		
	</head>
	<body>
		<div id='demo'>			
			<h3><span class="label label-info">Product Exploration Demo</span></h3>	
			
			<div id='main_searchbar' class="input-group">
				<input id='main_search_text' type="text" class="form-control" style="width: 350px" placeholder="Please enter product names, brands, etc.">
				<button id='search_btn' type="button" class="btn btn-info">Search</button>
				<button id='advance_btn' class='btn'>advanced >></button>
			</div>
				
			<div id='advanced_searchbar' style='display:none'> 
			</div>
			
			<div id='result'>Result</div>
			<div id='products_wrapper'></div>
		</div>
		
	</body>
	
	
	<script src="//code.jquery.com/jquery-1.9.1.js"></script>
	<script src="//code.jquery.com/ui/1.10.4/jquery-ui.js"></script>
	<script type='text/javascript' src='js/search.js'></script>
	<script type='text/javascript' src='js/main.js'></script>		
	<link rel="stylesheet" href="//code.jquery.com/ui/1.10.4/themes/smoothness/jquery-ui.css">
	<link rel='stylesheet' type='text/css' href='css/main.css' />
	<link rel='stylesheet' type='text/css' href='css/search.css' />
	<link rel='stylesheet' type='text/css' href='../common/css/basic.css' />
	<!-- Bootstrap -->				
	<script type='text/javascript' src='js/bootstrap/dist/js/bootstrap.js'></script>
	<link rel='stylesheet' type='text/css' href='js/bootstrap/dist/css/bootstrap.css' />
	<link rel='stylesheet' type='text/css' href='js/bootstrap/dist/css/bootstrap-theme.css' />
</html>

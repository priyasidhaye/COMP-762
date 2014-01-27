var advanced_search = {};
advanced_search.options = ['name', 'all_names', 'bottomLine', 'brand', 'description', 'displayName', 'highs', 'lows', 'rating_descriptions', 'rating_names', 'review', 'spec_descriptions', 'spec_names', 'summary'];
var is_advanced_search = true;

$.each(advanced_search.options, function() {
var checkbox = $('<div>').addClass('input-group').addClass('advanced-option').appendTo($("#advanced_searchbar"));
var name = $('<span>').addClass('input-group-addon').text(this.charAt(0).toUpperCase() + this.slice(1)).appendTo(checkbox);
var input = $('<input>').attr('type','text').attr('name', this).addClass('form-control').appendTo(checkbox);
});

$('#advance_btn').on('click', function() {
	clear();
	$('#advanced_searchbar').toggle();
	is_advanced_search = !is_advanced_search;
});

function clear() {
	$('input').each(function(){
	$(this).val('');});
}

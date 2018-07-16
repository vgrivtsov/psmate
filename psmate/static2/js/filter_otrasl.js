 //Filter otrasl
$('select#otrasl-filter').change(function() {
	var filterValue = $(this).val();
 filterList(filterValue);
});

// Otrasl filter function
function filterList(value) {
	var list = $(".jobtitlelist-details");

	$(list).hide();

	if (value == "All") {
		$(".jobtitlelist").find(".jobtitlelist-details").each(function (i) {
			$(this).show();
		});
	} else {


		$(".jobtitlelist").find('li[name="'+ value +'"]').each(function (i) {
   $(this).show();
   console.log(this);
		});
	}
}
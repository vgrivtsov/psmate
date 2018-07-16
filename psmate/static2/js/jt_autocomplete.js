$("#jtsearch").autocomplete({
	minLength: 3,
 delay: 500,

	source: function(req, add){
		var search=$("#jtsearch").val();
		$.ajax({
			url: '/jt-autocomplete/',
   async: true,
			dataType: 'json',
			type: 'GET',
			data: {'search': search,},
			success: function(data){
				var suggestions=[];

				$.each(data, function(index, object){
					suggestions.push(object.jobtitle);
				});

				add(suggestions);

			},
			error: function(){
				alert("Error!");
			}
		});
	}
});
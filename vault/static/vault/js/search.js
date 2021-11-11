const searchForm = $("#searchForm")
searchForm.submit(function(e){
	e.preventDefault();
	const word = $("#searchWord").val()
	//using django hardcoded urls.
	let url = `/vault/search/${word}`
	window.location =  url
})
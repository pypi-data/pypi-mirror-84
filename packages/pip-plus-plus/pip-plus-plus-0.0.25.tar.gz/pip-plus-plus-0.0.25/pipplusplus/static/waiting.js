$(document).ready(function () {
	setInterval(function(){
	let stat = "Processed"
	let id = "";
	let url = window.location.href;
	id = url.split("=")[1];
	
	$.ajax("/status?id=" + id, {
    type: 'GET',  // http method
    success: function (data, status, xhr) {
				let json_data = JSON.parse(data);
				stat = json_data["status"];
				if(stat == "Done") {
					let page = json_data["page"]
					let msg = json_data["msg"]
					if (msg == "None") {
						window.location.replace( "/" + page)
					} else {
						window.location.replace( "/" + page + "/" + msg);
					}
				}
			},
    error: function (jqXhr, textStatus, errorMessage) {
				console.log("Checking status again");
			}
	});
}, 2000)
});

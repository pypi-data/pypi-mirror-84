function GetData() {
	id = Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 7);
	option_name = document.getElementById("option").value
	packgeName = document.getElementById("package-name").value
	httpProxy = document.getElementById("http-proxy").value
	httpsProxy = document.getElementById("https-proxy").value
	json_to_send = {
		"id": id,
		"option": option_name,
		"package": packgeName,
		"http-proxy": httpProxy,
		"https-proxy": httpsProxy
	}
	return json_to_send
}
	

function SubmitReq() {
	let xhr = new XMLHttpRequest();
	xhr.onreadystatechange  = function() {
		let data = JSON.parse(this.responseText)
		let stat = data["status"]
		if (stat == "Processed") {
			window.location.replace("/waiting?id=" + id)
		}
		else {
			let page = data["page"]
			let msg = data["msg"]
			if (msg == "None") {
				window.location.replace( "/" + page + "?id=" + id)
			} else {
				window.location.replace( "/" + page + "/" + msg);
			}
		}
	};
	xhr.open("POST", "/submit", true);
	xhr.setRequestHeader('Content-Type', 'application/json');
	xhr.send(JSON.stringify(GetData()));
}
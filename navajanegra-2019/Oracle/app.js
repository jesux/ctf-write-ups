async function createhtml(msg) {
	if (msg !="") {
		let r = await fetch("/createhtml", {
			headers: {
				'Accept': 'application/json',
				'Content-Tipe': 'application/json'
			},
			method: "POST",
			body: JSON.stringify({html: msg})
		});
		let html = await r.text();
		return html
	}
}

async function adminsearch(q) {
	if (q != "") {
		let r = await fetch("/admin/search/" + encodeURIComponent(q));
		let html = await r.text();
		return html;
	}
}

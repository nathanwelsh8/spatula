/* Since django generates HTML elements automatically js needed to add bootstrap form classes to form elements */
function setClasses() {
	var name = document.getElementById("id_name");
    var category = document.getElementById("id_category");
    var toolsreq = document.getElementById("id_toolsreq");
	var diettype = document.getElementById("id_diettype");
	var cost = document.getElementById("id_cost");
	var difficulty = document.getElementById("id_difficulty");
	var ingredients = document.getElementById("id_ingredients");
	var method = document.getElementById("id_method");
	var id_form_0 = document.getElementById("id_form-0-image");
	var id_form_1 = document.getElementById("id_form-1-image");
	var id_form_2 = document.getElementById("id_form-2-image");



	name.classList.add("form-control");
    category.classList.add("form-control");
    toolsreq.classList.add("form-control");
	cost.classList.add("form-control");
	difficulty.classList.add("form-control");
	diettype.classList.add("form-control");
	ingredients.classList.add("form-control");
	method.classList.add("form-control");
	id_form_0.classList.add("form-control-file")
	id_form_1.classList.add("form-control-file")
	id_form_2.classList.add("form-control-file")
}
window.onload=setClasses;
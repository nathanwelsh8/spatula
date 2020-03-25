/* functions to be included in base.html file here */

function showSignin(){
    var x = document.getElementById("container");
	var y = document.querySelector('.sidenav p')
    if(x.style.top == "50px"){
        x.style.top= "-125px";
    }else{ 
        x.style.top= "50px";
    }
	
	if(y.style.marginTop == "0px"){
		y.style.marginTop = "170px";
	}else{
		y.style.marginTop = "0px"; 
    }

}

/*These  are the functions causing problems with inline styling*/
function showFilters(){
    var x = document.getElementById("sidebar");
    if(x.style.display=="none"){
        x.style.display="block";
    }else{
        x.style.display = "none";
    }
}

function showSearch(){
    var x = document.getElementById("searchbar")
	var y = document.getElementById("header")
    if(x.style.display=="none"){
        x.style.display="block";
		y.style.height="90px";
    }else{
        x.style.display="none";
		y.style.height="50px";
    }
}



/* functions to be included in base.html file here */

function sendRequest(text,sort,diet,categories){

    if (sort == undefined){

        $.get(window.location.href,
        {
            'search':text,
        },
        function(data){
            
            $('#recipies').html(data);
        });

    }else{
    $.get('/',
        {
            'search':text,
            'sorttype':sort,
            'diettype':diet,
            'categories':categories
        },
        function(data){
            
            $('#recipies').html(data);
        });
    }
        
}

function getSearchText(){
    return $('#searchbar').val();
}

function openNav() {
	var x = document.getElementById("mySidenav");
	var y = document.getElementById("container");
	var z = document.querySelector('.sidenav p')
	if(x.style.width == "0px"){ 
		x.style.width = "250px";
	}else{
		if (y.style.top == "50px"){
			y.style.top =  "-125px";
			z.style.marginTop = "0px";
		}
		x.style.width = "0px"; 
	}
}

function closeNav() {
	document.getElementById("mySidenav").style.width = "0";
} 
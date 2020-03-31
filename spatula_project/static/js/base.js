/* functions to be included in base.html file here */

$(document).ready(function(){ 
    $('#searchbar').on('keydown', function(e) {
        if (e.which == 13 ||e.keyCode == 13) {
            text = getSearchText();
            if (text.length >0){
                
                //sendRequest(getSearchText());
                console.log("base enter query sent");
                window.location ='/?redirect_search_text='+text;
            }
        }
    });
});


function showSignin(){
    var x = document.getElementById("container");
	var y = document.querySelector('.sidenav p')
    if(x.style.top == "-200px" & window.matchMedia('(max-device-width: 1024px)').matches){
        x.style.top= "100px";
    }else if(x.style.top == "-200px" & window.matchMedia('(min-device-width: 1024px)').matches){ 
        x.style.top= "50px";
    }else{
		x.style.top = "-200px";
	}
	
	if(y.style.marginTop == "0px" & x.style.top != "-200px" ){
		y.style.marginTop = "260px";
	}else{
		y.style.marginTop = "0px"; 
    }

}

function showFilters(){
    var x = document.getElementById("sidebar");
    if(x.style.display=="block"){
        x.style.display="none";
    }else{
        x.style.display = "block";
    }
}

function showSearch(){
    var x = document.getElementById("searchbar")
	var y = document.getElementById("header")
    if(x.style.display=="block"){
        x.style.display="none";
		y.style.height="100px";
    }else{
		x.style.display="block";
		y.style.height="170px";

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


function getSortType(){
    return $('input:radio[name=sort]:checked').val();
}

function getDietType(){
    var selected = [];
    $('#meat input:checked').each(function(){
        if (this.checked){     
            selected.push($(this).attr('name'));
        }
    });
    return selected;
}

function getCategories(){
    var categories = [];
    $('#categories input:checked').each(function(){
        categories.push($(this).attr('name'));
    });
    return categories;
}


function openNav() {
	var x = document.getElementById("mySidenav");
	var y = document.getElementById("container");
	var z = document.querySelector('.sidenav p')
	if(x.style.width == "0px"){ 
		x.style.width = "500px";
	}else{
		if (y.style.top == "100px"){
			y.style.top =  "-200px";
			z.style.marginTop = "0px";
		}
		x.style.width = "0px"; 
	}
}
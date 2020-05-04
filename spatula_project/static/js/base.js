/* functions to be included in base.html file here */

$(document).ready(function(){ 
    $('#searchbar').on('keydown', function(e) {
        if (e.which == 13 ||e.keyCode == 13) {
            text = getSearchText();
            if (text.length >0){
                window.location ='/?redirect_search_text='+text;
            }
        }
    });

   
});

/*Show signin container when button clicked */
function showSignin(){
    var x = document.getElementById("container");
	var y = document.querySelector('.sidenav p')
	var w = window.outerWidth;
	/* Need two different logic statements for mobile and desktop view since headers are different sizes*/ 
    if(x.style.top == "-200px" && (window.matchMedia('(max-device-width: 1024px)').matches || w < 1040)){
        x.style.top= "100px";
    }else if(x.style.top == "-200px" && (window.matchMedia('(min-device-width: 1024px)').matches && w > 1040)){ 
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

/* Show filters on mobile view when button clicked */
function showFilters(){
    var x = document.getElementById("sidebar");
    if(x.style.display=="block"){
        x.style.display="none";
    }else{
        x.style.display = "block";
    }
}

/* Show searchbar when button clicked on mobile view */
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

/* Open sidenav on mobile view*/
function openNav() {
	var x = document.getElementById("mobile_sidenav");
	var y = document.getElementById("container");
	var z = document.querySelector('.sidenav p');
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


function tempDisplayMessage(id,content="", contentAfter="",time=2000, remainVisible){
    if (id){
        $("#"+id).html(content);
            document.getElementById(id).style.visibility = 'visible';

            setTimeout(function(){
                if (remainVisible == false){
                    document.getElementById(id).style.visibility = 'hidden';
                }
                $("#"+id).html(contentAfter);
            }, time);

    }
}

function is_large_tablet_device(loc){
    var w = window.outerWidth
    
    if (w >=1024){ // dealing with hd tablet
    
        window.location.href = "https://www.google.com"
        
    }
    
}
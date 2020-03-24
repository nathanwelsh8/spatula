/* functions to be included in base.html file here */

function sendRequest(text,sort,diet,categories){

    if (sort == undefined){

        $.get(window.location.href,
        {
            'search':text,
        },
        function(data){
            console.log(data);
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
            console.log(data);
            $('#recipies').html(data);
        });
    }
        
}

function getSearchText(){
    return $('#searchbar').val();
}


function showSignin(){
    var x = document.getElementById("container");
    if(x.style.display=="none"){
        x.style.display="block";
    }else{
        x.style.display="none";
    }
}

function openNav() {
	document.getElementById("mySidenav").style.width = "250px";
}

function closeNav() {
	document.getElementById("mySidenav").style.width = "0";
} 
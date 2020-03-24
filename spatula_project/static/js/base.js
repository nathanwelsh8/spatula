/* functions to be included in base.html file here */

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
/* functions to be included in base.html file here */

function showSignin(){
    var x = document.getElementById("container");
    if(x.style.top == "50px"){
        x.style.top= "-78px";
    }else{
        x.style.top= "50px";
    }
}
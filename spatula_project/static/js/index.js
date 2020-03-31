$(document).ready(function(){ 
    
    console.log("Document ready");
    var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    console.log("is a mobile device:"+isMobile);
    $("#searchbar").keyup(function() {
        console.log("search bar trigger");
        sendRequest(getSearchText(),getSortType(), getDietType(), getCategories());
        
    });

    // add the filters now

    $('input[type="radio"]').click(function(){
        console.log("radio trigger");
        sendRequest(getSearchText(),getSortType(), getDietType(), getCategories());
    });

    $('input[type="checkbox"]').click(function(){
        console.log("checkbox trigger");
        sendRequest(getSearchText(),getSortType(), getDietType(), getCategories());
    });

    /** There is a bug where if the window is shrunk 
     *  and then resized the filter menu dissappears 
     *  detect window resize and re-add filter menu.
    */
    document.getElementsByTagName("BODY")[0].onresize = function() {resetCss()};
    
});
    


/**
 * If the window is do be styles desktop mode then
 * revert overwritten css to desktop mode. 
 * Only make this change if the window size was
 * previously less than 550px
 */
var previous_size = 550;
function resetCss(){
    var w = window.outerWidth;
    console.log("current "+w+"| prev "+previous_size);
    if(w >= 550 & previous_size <550){
        var search_bar = document.getElementById("searchbar");
        var side_bar = document.getElementById("sidebar");
        var header = document.getElementById("header");
		search_bar.removeAttribute("style");
        side_bar.removeAttribute("style");
        header.removeAttribute("style");
        console.log("css reset");
    }
    previous_size = w;

}
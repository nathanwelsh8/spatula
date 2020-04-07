$(document).ready(function(){ 
    
    var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    $("#searchbar").keyup(function() {
        sendRequest(getSearchText(),getSortType(), getDietType(), getCategories());
        
    });

    // add the filters now

    $('input[type="radio"]').click(function(){
        sendRequest(getSearchText(),getSortType(), getDietType(), getCategories());
    });

    $('input[type="checkbox"]').click(function(){
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
   
    if(w >= 550 & previous_size <550){
        var search_bar = document.getElementById("searchbar");
        var side_bar = document.getElementById("sidebar");
        var header = document.getElementById("header");
		search_bar.removeAttribute("style");
        side_bar.removeAttribute("style");
        header.removeAttribute("style");
        
    }
    previous_size = w;

}
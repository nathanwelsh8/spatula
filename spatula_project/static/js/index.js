$(document).ready(function(){ 
    // perform a quick load
    sendRequest(getSearchText(),getSortType(), getDietType(), getCategories());
    console.log("Document ready");
    var isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
    console.log("is a mobile device:"+isMobile);
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
        search_bar.style.display = "inline-block";
        side_bar.style.display = "block";
        header.style.height="50px";
        console.log("css reset");
    }   
    previous_size = w;

}
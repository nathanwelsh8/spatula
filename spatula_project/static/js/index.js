$(document).ready(function(){ 
    // perform a quick load
    sendRequest(getSearchText(),getSortType(), getDietType(), getCategories());
    console.log("Document ready");

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
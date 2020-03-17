$(document).ready(function(){ 
    console.log("Document ready");

    $("#searchbar").keyup(function() {
        
        sendRequest();
        
    });

    // add the filters now

    $('input[type="radio"]').click(function(){
        console.log("Radio button pressed");
    	var demovalue = $(this).val();
        sendRequest();
    });

    $('input[type="checkbox"]').click(function(){
        console.log("Checkbox pressed");
        sendRequest();
    });

    
});

 function sendRequest(){

    var searchText = getSearchText();
    var sortType   = getSortType(); 
    var dietType   = getDietType(); // array of acceptable diets
    var categories = getCategories(); // array of acceptable categories
    console.log(dietType);
    $.get('/',
        {
            'search':searchText,
            'sorttype':sortType,
            'diettype':dietType,
            'categories':categories
        },
        function(data){
            console.log(data);
            $('#recipies').html(data);
        });
        
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
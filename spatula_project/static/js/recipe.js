function update_recipe(){

    var csrf = $('input:hidden[name=csrfmiddlewaretoken]').val();

    var difficulty = $('#edit_difficulty').val();
    var cost = $('#edit_cost').val();
    var tools = $('#edit_tools').val();
    var ingredients = $('#edit_ingredients').val();
    var method = $('#edit_method').val();

    // this is not the correct way to find the diet choice but using it to bug fix
    var diet =  $('input:radio[name=exampleRadios]:checked').val()
    var category = $('#edit_category option:selected').val();
    var portion = $('#edit_portionsize option:selected').val();
    var cooktime = $('#edit_cooktime option:selected').val();



    $.post(window.location.href,
        {
            'csrfmiddlewaretoken': csrf,
            'update_recipe': true,
            'difficulty': difficulty,
            'cost': cost,
            'diet': diet,
            'portionsize':portion,
            'cooktime':cooktime,
            'category': category,
            'tools': tools,
            'ingredients': ingredients,
            'method': method,
            
        },
        function(data){
            // tell the user that there data was updated
            $("#recipe_success_msg").html("Recipe updated sucessfully!");
            document.getElementById('recipe_success_msg').style.visibility = 'visible';

            setTimeout(function(){
                document.getElementById('recipe_success_msg').style.visibility = 'hidden';
                $("#recipe_success_msg").html("");
            }, 2000);
        } 
        );
}

function toggle_edit_view(bool){
    $.get(window.location.href,
        {
            'toggle_edit_view':true,
            'csrfmiddlewaretoken': $('input:hidden[name=csrfmiddlewaretoken]').val(),

    },
    function(htmldata){
        window.location.href = window.location.href + "?toggle_edit_view="+bool;
        if (bool =="False"){
            window.location.href = window.location.href.replace(window.location.search,'');
        }
        
    }
    );
}
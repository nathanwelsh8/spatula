$(document).ready(function(){
});    

function update_recipe(){

    var csrf = $('input:hidden[name=csrfmiddlewaretoken]').val();

    var difficulty = $('#edit_difficulty').val();
    var cost = $('#edit_cost').val();
    var tools = $('#edit_tools').val();
    var ingredients = $('#edit_ingredients').val();
    var method = $('#edit_method').val();

    // this is not the correct way to find the diet choice but using it to bug fix
    var diet = $('#edit_category option:selected').val();
    var category = $('#edit_category option:selected').val();
    
    

    $.post(window.location.href,
        {
            'csrfmiddlewaretoken': csrf,
            'update_recipe': true,
            'difficulty': difficulty,
            'cost': cost,
            'diet': diet,
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
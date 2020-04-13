$(document).ready(function(){

    /* this method fetches data from the db.
        hackers, I see you have you tried replacing 
        getUser with getUserAll? 
    */

    getUserData();

    $("#searchbar").keyup(function() {
        sendRequest(getSearchText());
    });

});    
function update_bio(){

    var csrf = $('input:hidden[name=csrfmiddlewaretoken]').val();
    var v = $('#edit_bio').val();
    $.post(window.location.href,
        {
            'csrfmiddlewaretoken': csrf,
            'update_bio': v
        },
        function(data){
            // tell the user that there data was updated
            tempDisplayMessage(id="bio_success_msg",content="Bio successfully updated!");
        } 
        );
}

function getUserData(param){
    $.get(window.location.href,
        {
            'get_recipes':"getUser"
        },
        function(data){
            $('#recipies').html(data);
        }
        );

}

// Security checks handled by view
delete_int = 0;
num_click = 3;
function deleteProfile(params){

    if (delete_int >=num_click){
        $.post(window.location.href,
            {
                'delete_profile':"True",
                'csrfmiddlewaretoken':$('input:hidden[name=csrfmiddlewaretoken]').val()
            },
            function(data){
                //redirect to index
                window.location = "/";
            }
        );
    }else{
        var id = 'delete_button';
        tempDisplayMessage(id=id,
            content="Click "+(num_click-delete_int)+" more times",
            contentAfter="Delete Account", time =5000, remainVisible=true);

        delete_int +=1;
    }
}

function tempDisplayMessage(id,content="", contentAfter="",time=2000, remainVisible){
    if (id){
        $("#"+id).html(content);
            document.getElementById(id).style.visibility = 'visible';

            setTimeout(function(){
                if (remainVisible == false){
                    document.getElementById(id).style.visibility = 'hidden';
                }
                $("#"+id).html(contentAfter);
            }, time);

    }
}

var del_recipe_counter = 0;
var del_recipe_click = 3;
var prev_id = null;
function deleteRecipe(id){
    if (del_recipe_counter>=del_recipe_click & id==prev_id){

        $.post(window.location.href,
            {
                'delete_recipe':id,
                'csrfmiddlewaretoken':$('input:hidden[name=csrfmiddlewaretoken]').val()
            },
            function(data){
                return getUserData();
            }
        );

        del_recipe_counter = 0;
    }else{
        prev_id = id;
        
        tempDisplayMessage(id=id,
                            content="Click "+(del_recipe_click-del_recipe_counter)+" more times",
                            contentAfter="Delete",time=5000,remainVisible=true);
        del_recipe_counter ++;
        
    }
}

function update_password(){
    var new_pass = $('#new_password').val();
    var conf_new_pass = $('#new_password_confirm').val();
    
    if (new_pass==conf_new_pass){
        var paswd=  /^(?=.*[0-9])[a-zA-Z0-9!@#$%^&*]{8,35}$/; // regex to match acceptable passwords
        if(new_pass.match(paswd)){
            $.post(window.location.href,
                {'update_password':true,
                'old_password':$('#old_password').val(),
                'new_password':new_pass,
                'csrfmiddlewaretoken':$('input:hidden[name=csrfmiddlewaretoken]').val()
                },
                function(data){
                    tempDisplayMessage(id="password_errors",data,'',10000,false)
                }
                );
        }else{
            tempDisplayMessage(id='password_errors','password must be 8-35 charcters with at least one uppercase and a number',
            "",10000,false);
        }
        
    }else{
        tempDisplayMessage(id="password_errors","Passwords do not match!",'',10000,false);
    }
}
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
    console.log(v+csrf);
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
    console.log(remainVisible);
    if (id){
        $("#"+id).html(content);
            document.getElementById(id).style.visibility = 'visible';

            setTimeout(function(){
                if (remainVisible == false){
                    console.log("hide after 2secs");
                    document.getElementById(id).style.visibility = 'hidden';
                }
                $("#"+id).html(contentAfter);
            }, time);

    }
}
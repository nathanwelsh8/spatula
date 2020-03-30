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
            $("#bio_success_msg").html("Details updated sucessfully!");
            document.getElementById('bio_success_msg').style.visibility = 'visible';

            setTimeout(function(){
                document.getElementById('bio_success_msg').style.visibility = 'hidden';
                $("#bio_success_msg").html("");
            }, 2000);
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

// Security checks handles by database. Insecure? heck ye
function deleteProfile(params){
    $.post(window.location.href,
        {
            'delete_profile':"True",
            'csrfmiddlewaretoken':$('input:hidden[name=csrfmiddlewaretoken]').val()
        },
        function(data){
            //redirect to index
            window.location = "/";
        }
        )
}
$(document).ready(function(){

        /* this method fetches data from the db.
            hackers, I see you have you tried replacing 
            getUser with getUserAll? 
        */
       console.log("sending get"+window.location.href);

        $.get(window.location.href,
            {
                'get_recipes':"getUser"
            },
            function(data){
                $('#recipies').html(data);
            }
            );

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
            $(".sucessfull_update").html("Details updated sucessfully!");
            document.getElementById('bio_success_msg').style.visibility = 'visible';

            setTimeout(function(){
                document.getElementById('bio_success_msg').style.visibility = 'hidden';
                $(".sucessfull_update").html("");
            }, 2000);
        } 
        );
}
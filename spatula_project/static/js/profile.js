
var run = 0;
$(document).ready(function(){

        /* this method fetches data from the db
            hackers i see you have you tried replacing 
            getUser with getUserAll? 
        */
       console.log("sending get"+window.location.href);

        $.get(window.location.href,
            {
                'get_recipes':"getUser"
            },
            function(data){
                run +=1;
                console.log("run:"+run);
                $('#recipies').html(data);

            }
            );
});
    
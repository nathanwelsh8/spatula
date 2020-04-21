function termsAccept(btn){
    
    var submitBttn = document.getElementById("register_button");
    if (btn.checked == true){
        submitBttn.disabled = false;
      }
    else{
        submitBttn.disabled = true;
    }
}

function disabledFeedback(btn){
    
    if(btn.disabled ==true){
        
        tempDisplayMessage(id="button_feedback",content="Please accept terms and conditions in order to register","",5000,false);
    }
}
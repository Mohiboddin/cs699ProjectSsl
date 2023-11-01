
// for Forgot password page

document.getElementById("forgotPassword").addEventListener("click", function(event){
    document.getElementById("emailCard").classList.add("hidden");
    showToast("Your Request is processing ", "info");
    event.preventDefault()
    console.log("for got password request")
    var email_val= document.getElementById("email").value
    // var password_val= document.getElementById("password").value
    data={
        "email": email_val    
    }
    console.log(data)
    validate_email=ValidateEmail(email_val)
    if (email_val && validate_email){

        // using Async and await
        
            fetch('/forgotpassword', {
            method: 'POST', // or 'PUT'
            headers: {
            "content-type": "application/json ;charset=utf-8",
            },
            body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data);
            if(data["code"]==1)
                {
                    document.getElementById("otpCard").classList.remove("hidden");        
                    // call modal
                    showToast("OTP has been sent to your email id, please enter it within 2 minute", "success");
                }
            else if(data["code"]==2){
                    // call modal
                    document.getElementById("emailCard").classList.remove("hidden");
    
                    showToast("The user dosen't exist.", "error");
            }
            
            else if(data["code"]==3)
                {   document.getElementById("emailCard").classList.remove("hidden");
                    showToast("Something went wrong", "error");
                }
            else if(data["code"]==4)
                {  
                    document.getElementById("otpCard").classList.remove("hidden");        
                    showToast("OTP already sent check email", "info");
        
                }
            })
            .catch((error) => {
            console.error('Error:', error);
            });

}

});



// for Forgot password page

document.getElementById("otpEntered").addEventListener("click", function(event){
    event.preventDefault()
    console.log("for got password request")
    var email_val= document.getElementById("email").value
    var otp_val= parseInt(document.getElementById("otp").value)
    // var password_val= document.getElementById("password").value
    data={
        "email": email_val,
        "otp": otp_val
    }
    console.log(data)
    validate_email=ValidateEmail(email_val)
    if (email_val && otp_val && validate_email){
        
            fetch('/otpverify', {
            method: 'POST', // or 'PUT'
            headers: {
            "content-type": "application/json ;charset=utf-8",
            },
            body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
            console.log('Success:', data);
            if(data["code"]==1)
                {
                    window.location.href = '/recovery';
                }
            else if(data["code"]==2){
                    // call modal
                    showToast("Wrong OTP Or the 2 min time limit exceeded try again.", 'error')
                    document.getElementById("otpCard").classList.add("hidden");    
                    document.getElementById("emailCard").classList.remove("hidden");        
    

    
            
            }
            
            })
            .catch((error) => {
            console.error('Error:', error);
            });

}

});



function ValidateEmail(mail) 
{
    console.log("in validate")
 if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
  {
    return (true)
  }

showToast("Email format incorrect","error");
    return (false)
}

function showToast(message, type) {
    const toastContainer = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.classList.add("text-white", "py-2", "px-4", "mb-2", "rounded");
    toast.innerText = message;

    const typeClasses = {
        success: "bg-green-500",
        error: "bg-red-500",
        info: "bg-blue-500"
      };
  
      // Apply type-specific classes, default to 'info' if type is not recognized
      toast.classList.add(typeClasses[type] || typeClasses.info);

    toastContainer.appendChild(toast);
    
    setTimeout(() => {
      toast.remove();
    }, 5000); // Remove the toast after 5 seconds (adjust as needed)
}

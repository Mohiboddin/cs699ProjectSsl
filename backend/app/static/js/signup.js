// for login page
document.getElementById("signup").addEventListener("click", function(event){
    event.preventDefault()
    console.log("Signup request")
    var email_val= document.getElementById("email").value
    var password_val= document.getElementById("password").value
    var username_val= document.getElementById("username").value
    data={
        "email": email_val,
        "password": password_val,
        "username": username_val
    }
    console.log(data)

    if (!email_val && !password_val && !username_val){
        showToast("Fill all the feilds properly", 'error');
    }

    valid_email=ValidateEmail(email_val)

    if (email_val && password_val && valid_email){

        // using Async and await
        
        document.getElementById("emailCard").classList.add("hidden");
        showToast("Your Request is processing ", "info");

            fetch('/signup', {
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
            else if (data["code"]==2)
                {    document.getElementById("emailCard").classList.remove("hidden");
                    console.log("Email Already exist"); 
                    showToast("Email Already exist, enter Different Email", "error");
                }
            else if (data["code"]==3)
            {    document.getElementById("emailCard").classList.remove("hidden");
                console.log("Somthing went wrong"); 
                showToast("Somthing went wrong try again after 2 min", "error");
            }
            })
            .catch((error) => {
            console.error('Error:', error);
            });

}

});


// aftr otp entered 

document.getElementById("signOtpEntered").addEventListener("click", function(event){
    event.preventDefault()
    console.log("OTP sending")

    var email_val= document.getElementById("email").value
    var password_val= document.getElementById("password").value
    var otp_val= parseInt(document.getElementById("otp").value)
    var username_val= document.getElementById("username").value
    data={
        "email": email_val,
        "password": password_val,
        "username": username_val,
        "otp": otp_val

    }
    console.log(data)

    if (!otp_val){
        showToast("Fill all the feilds properly", 'error');
    }
   
    validate_email=ValidateEmail(email_val)
    if (email_val && otp_val && validate_email){
        
            fetch('/signupotpverify', {
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
                    showToastAndRedirect("Account created.", 'success')
                    
                }
            else if(data["code"]==2){
                    // call modal
                    showToast("Wrong OTP Or the 2 min time limit exceeded try again after 2min.", 'error')
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
  console.log("Invalid email");
showToast("Email format is Incorrect", "error");
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


function showToastAndRedirect(message, type) {
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
      window.location.href = '/login';
    }, 2000); // Remove the toast after 5 seconds (adjust as needed)
}
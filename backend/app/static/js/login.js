// for login page
document.getElementById("signin").addEventListener("click", function(event){
    event.preventDefault()
    console.log("Signin request")
    var email_val= document.getElementById("email").value
    var password_val= document.getElementById("password").value
    data={
        "email": email_val,
        "password": password_val
    }
    console.log(data)

    valid_email=ValidateEmail(email_val)

    if ((!email_val) || (!password_val)){
        showToast("Fill all the fields properly", 'error');
    }

    if (email_val && password_val && valid_email){

        // using Async and await
        

            fetch('/login', {
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
                window.location.href = '/dashboard';
            else
                {
                    console.log("Invalid user name or password"); 
                    showToast("Invalid Emial or Password", "error");
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
// for login page
document.getElementById("change_password").addEventListener("click", function(event){
    event.preventDefault()
    console.log("Password change request")
    var password_val= document.getElementById("password").value
    var confirm_password_val= document.getElementById("confirm_password").value
    data={
        "password": password_val,
        "confirm_password": confirm_password_val
    }
    console.log(data)

    if ((!password_val) || (!confirm_password_val)){
        showToast("Fill all the fields properly", 'error');
    }


    if(password_val===confirm_password_val)
    {

        if (password_val && confirm_password_val){

            // using Async and await
            
    
                fetch('/recovery', {
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
                    window.location.href = '/login';
                else
                    {
                        showToast('Request for OTP again, OTP expired','info');
                    }
                })
                .catch((error) => {
                console.error('Error:', error);
                });
    
    }
    else{
        showToast('Enter Data','info');
    }

    }
    else{
        showToast('password and Confirrmed Password not matched','error');
    }

   

});


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
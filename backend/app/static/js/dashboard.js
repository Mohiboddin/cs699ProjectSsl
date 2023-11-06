// for login page
document.getElementById("addURLButton").addEventListener("click", function(event){
    event.preventDefault()
    console.log("new url request")
    var newUrl_val= document.getElementById("newUrl").value
    var newNotifyBefore_val= document.getElementById("newNotifyBefore").value
    data={
        "url": newUrl_val,
        "notifybefore": newNotifyBefore_val
    }
    console.log(data)

    if (newUrl_val && newNotifyBefore_val){

        // using Async and await
        

            fetch('/certificate_info', {
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
                    showToast(data["msg"], "success");
                }
            else if(data["code"]==2 || data["code"]==3)
            {
                showToast(data["msg"], "error");
            }
            })
            .catch((error) => {
            console.error('Error:', error);
            });

}

});


//---------------------------------------------------------

let storedValue;
let row;

// Add a click event listener to all elements with the "delete" class
const deleteButtons = document.querySelectorAll('.delete');

deleteButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default link behavior

    // Retrieve the value associated with the clicked row
    value = button.getAttribute('data-value');
     row = button.closest('tr');
                   

    // Now, you can use the 'value' in your JavaScript function or pass it to an API, etc.
    console.log('Value:', value);
  });
});



document.getElementById("deleteURLButton").addEventListener("click", function(event){
    event.preventDefault()
    console.log("new url request")
    var delURLVal= value
    data={
        "id": delURLVal,
    }
    console.log(data)

    if (delURLVal ){

        // using Async and await
        

            fetch('/certificate_info', {
            method: 'DELETE', // or 'PUT'
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
                    showToast(data["msg"], "success");
                    if (row) {
                        row.remove();
                      }

                }
            else if(data["code"]==2)
            {
                showToast(data["msg"], "error");
            }
            })
            .catch((error) => {
            console.error('Error:', error);
            });

}

});



//---------------------------------------------------------------



//---------------------------------------------------------

let editrow;
const rowData = [];

// Add a click event listener to all elements with the "delete" class
const updateButtons = document.querySelectorAll('.edit');

updateButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default link behavior

    // Retrieve the value associated with the clicked row
    storedValue = button.getAttribute('data-value');
    editrow = button.closest('tr');

    console.log(editrow)

    if (editrow) {
        // Capture all the values in the row
        const cells = editrow.querySelectorAll('td');

        cells.forEach((cell) => {
          rowData.push(cell.textContent);
        });
  
        // Now, you have all the values in the 'rowData' array
        console.log('Row Data:', rowData);
                   
    }
    console.log('Value:', storedValue);
    if (rowData[5].toLowerCase() === 'false') {
        // If the value in rowData[5] is 'false', hide the "noCerti" div
        const noCertiDiv = document.getElementById('noCertiIssue');
      
        if (noCertiDiv) {
          noCertiDiv.style.display = 'none';
        }
      }
      else{
        const noCertiDiv = document.getElementById('certiIssue');
      
        if (noCertiDiv) {
          noCertiDiv.style.display = 'none';
        }
      }



  });
});



document.getElementById("deleteURLButton").addEventListener("click", function(event){
    event.preventDefault()
    console.log("new url request")
    var delURLVal= value
    data={
        "id": delURLVal,
    }
    console.log(data)

    if (delURLVal ){

        // using Async and await
        

            fetch('/certificate_info', {
            method: 'DELETE', // or 'PUT'
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
                    showToast(data["msg"], "success");
                    if (row) {
                        row.remove();
                      }

                }
            else if(data["code"]==2)
            {
                showToast(data["msg"], "error");
            }
            })
            .catch((error) => {
            console.error('Error:', error);
            });

}

});





function showToast(message, type) {
    var toastContainer = document.getElementById("snackbar");
    toastContainer.className = "show";
    toastContainer.innerText = message;

    const typeStyles = {
        success: {
            backgroundColor: "#04960b", // Green
            color: "white",
        },
        error: {
            backgroundColor: "#EF4444", // Red
            color: "white",
        },
        info: {
            backgroundColor: "#3B82F6", // Blue
            color: "white",
        },
    };

    const style = typeStyles[type] || typeStyles.info;
    toastContainer.style.backgroundColor = style.backgroundColor;
    toastContainer.style.color = style.color;


    setTimeout(function(){ toastContainer.className = toastContainer.className.replace("show", ""); }, 3000);
  }

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
        
        showToast('the request can take some time', "info");
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
                {   fetchAndDisplayCertificateInfo();
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
deleteButtons = document.querySelectorAll('.delete');

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




//delete message feature
// Add a click event listener to all elements with the "delete" class
deleteMessageButtons = document.querySelectorAll('.deletemessage');

deleteMessageButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default link behavior

    // Retrieve the value associated with the clicked row
    value = button.getAttribute('data-value');
     row = button.closest('tr');
     

    // Now, you can use the 'value' in your JavaScript function or pass it to an API, etc.
    console.log('Value:', value);
     
    data={
        "id": value,
    
    }

    // using Async and await
        

    fetch('/notificationdelete', {
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
  });
});

//---------------------------------------------------------------



//---------------------------------------------------------

let editrow;
rowData = [];
certi_status=false;
url=""
// Add a click event listener to all elements with the "delete" class
updateButtons = document.querySelectorAll('.edit');

updateButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default link behavior

    // Retrieve the value associated with the clicked row
    storedValue = button.getAttribute('data-value');
    editrow = button.closest('tr');

    console.log(editrow)

    if (editrow) {
        // Capture all the values in the row
        cells = editrow.querySelectorAll('td');
        rowData=[]
        cells.forEach((cell) => {
          rowData.push(cell.textContent);
        });
  
        // Now, you have all the values in the 'rowData' array
        console.log('Row Data:', rowData);
                   
    }
    console.log('Value:', storedValue);
    url=rowData[0]
    if (rowData[5].toLowerCase() === 'false') {

        var urlTextElement = document.querySelector('.urlText2');

        // Check if the element is found
        if (urlTextElement) {
            // Change the content of the <p> element
            urlTextElement.textContent = url;
        }
        // If the value in rowData[5] is 'false', hide the "noCerti" div
        noCertiDiv = document.getElementById('noCertiIssue');
        certi_status=false;
        if (noCertiDiv) {
          noCertiDiv.style.display = 'none';
        }
        noCertiDiv = document.getElementById('certiIssue');
        if (noCertiDiv) {
          noCertiDiv.style.display = 'block';
        }
        
      }
      else{

        var urlTextElement = document.querySelector('.urlText1');

        // Check if the element is found
        if (urlTextElement) {
            // Change the content of the <p> element
            urlTextElement.textContent = url;
        }
        noCertiDiv = document.getElementById('noCertiIssue');
        certi_status=false;
        if (noCertiDiv) {
          noCertiDiv.style.display = 'block';
        }


        noCertiDiv = document.getElementById('certiIssue');
        certi_status=true;
        if (noCertiDiv) {
          noCertiDiv.style.display = 'none';
        }
      }



  });
});



document.getElementById("updateUrlModal").addEventListener("click", function(event){
    
    event.preventDefault()
    console.log("update url request")
    var updateURLVal= storedValue

    if(certi_status==false){
        data={
            "url":url,
            "id": updateURLVal,
            "certi_status": certi_status
            
        }
    }
    else{
        var updateNotifyBefore_val= document.getElementById("updateNotifyBefore").value
        if (updateNotifyBefore_val <= 1) {
            showToast("Notify before value should be greater then  1", "error");
            console.log("updateNotifyBefore should be greater than 1");
            return;  // This will exit the function without returning a value
        }
        
        data={
            "url":url,
            "id": updateURLVal,
            "certi_status": certi_status,
            "updateNotifyBefore_val": updateNotifyBefore_val
            
        }
    }

    console.log(data)

    if (updateURLVal ){

        // using Async and await
        showToast('the request can take some time', "info");

            savedrow= editrow;
            fetch('/certificate_info', {
            method: 'PUT', // or 'PUT'
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

                    fetchAndDisplayCertificateInfo();

                    if (savedrow) {
                        console.log(savedrow.cells[3].textContent);
                        savedrow.cells[3].textContent = updateNotifyBefore_val;
                      }
                      if (certi_status==false)
                      {
                        savedrow.cells[5].textContent = "Ture";
                      }

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


  // Fetch and display certificate info
function fetchAndDisplayCertificateInfo() {
    fetch('/certificate_info', {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        if (data.code === 1) {
            // Render the HTML with the certificate info
            renderCertificateInfo(data.msg);
        } else {
            showToast(data.msg, 'error');
        }
    });
}

// Render certificate info in HTML table
function renderCertificateInfo(certificateInfo) {
    tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = ''; // Clear existing content
    console.log(certificateInfo);
    certificateInfo.forEach(cert => {
        row = document.createElement('tr');
        row.innerHTML = `
            <td>${cert[0]}</td>
            <td>${cert[1]}</td>
            <td>${cert[2]}</td>
            <td>${cert[3]}</td>
            <td>${cert[4]}</td>
            <td>${cert[5]}</td>
            <td>
				<a data-value="${cert[7]}" href="#editUrlModal" class="edit" data-toggle="modal"><i class="material-icons" data-toggle="tooltip" title="Edit">&#xE254;</i></a>
				<a data-value="${cert[7]}" href="#deleteUrlModal" class="delete" data-toggle="modal"  ><i class="material-icons" data-toggle="tooltip" title="Delete">&#xE872;</i></a>
			</td>
        `;
        tableBody.appendChild(row);

    });

       //adding events:
       deleteButtons = document.querySelectorAll('.delete');

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
       
       updateButtons = document.querySelectorAll('.edit');

updateButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault(); // Prevent the default link behavior

    // Retrieve the value associated with the clicked row
    storedValue = button.getAttribute('data-value');
    editrow = button.closest('tr');

    console.log(editrow)

    if (editrow) {
        // Capture all the values in the row
        cells = editrow.querySelectorAll('td');
        rowData=[]
        cells.forEach((cell) => {
          rowData.push(cell.textContent);
        });
  
        // Now, you have all the values in the 'rowData' array
        console.log('Row Data:', rowData);
                   
    }
    console.log('Value:', storedValue);
    url=rowData[0]
    if (rowData[5].toLowerCase() === 'false') {

        var urlTextElement = document.querySelector('.urlText2');

        // Check if the element is found
        if (urlTextElement) {
            // Change the content of the <p> element
            urlTextElement.textContent = url;
        }
        // If the value in rowData[5] is 'false', hide the "noCerti" div
        noCertiDiv = document.getElementById('noCertiIssue');
        certi_status=false;
        if (noCertiDiv) {
          noCertiDiv.style.display = 'none';
        }
        noCertiDiv = document.getElementById('certiIssue');
        if (noCertiDiv) {
          noCertiDiv.style.display = 'block';
        }
        
      }
      else{

        var urlTextElement = document.querySelector('.urlText1');

        // Check if the element is found
        if (urlTextElement) {
            // Change the content of the <p> element
            urlTextElement.textContent = url;
        }
        noCertiDiv = document.getElementById('noCertiIssue');
        certi_status=false;
        if (noCertiDiv) {
          noCertiDiv.style.display = 'block';
        }


        noCertiDiv = document.getElementById('certiIssue');
        certi_status=true;
        if (noCertiDiv) {
          noCertiDiv.style.display = 'none';
        }
      }



  });
});



document.getElementById("updateUrlModal").addEventListener("click", function(event){
    
    event.preventDefault()
    console.log("update url request")
    var updateURLVal= storedValue

    if(certi_status==false){
        data={
            "url":url,
            "id": updateURLVal,
            "certi_status": certi_status
            
        }
    }
    else{
        var updateNotifyBefore_val= document.getElementById("updateNotifyBefore").value
        if (updateNotifyBefore_val <= 1) {
            showToast("Notify before value should be greater then  1", "error");
            console.log("updateNotifyBefore should be greater than 1");
            return;  // This will exit the function without returning a value
        }
        
        data={
            "url":url,
            "id": updateURLVal,
            "certi_status": certi_status,
            "updateNotifyBefore_val": updateNotifyBefore_val
            
        }
    }

    console.log(data)

    if (updateURLVal ){

        // using Async and await
        showToast('the request can take some time', "info");
            savedrow= editrow;
            fetch('/certificate_info', {
            method: 'PUT', // or 'PUT'
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

                    fetchAndDisplayCertificateInfo();

                    if (savedrow) {
                        console.log(savedrow.cells[3].textContent);
                        savedrow.cells[3].textContent = updateNotifyBefore_val;
                      }
                      if (certi_status==false)
                      {
                        savedrow.cells[5].textContent = "Ture";
                      }

                }
            else if(data["code"]==2 || data["code"]==3)
            {   console.log(data["msg"]);
                showToast(data["msg"], "error");
            }
            
            })
            .catch((error) => {
            console.error('Error:', error);
            });

}

});


     
}





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

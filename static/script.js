// Function to trigger the file input dialog
function cho() {
  document.getElementById("file").click(); // Simulate a click on the hidden file input
}

// Event listener for file input change (file selection)
document.getElementById("file").addEventListener("change", () => {
  const fileInput = document.getElementById("file");
  const file = fileInput.files[0]; // Get the selected file

  if (file) {
    // Display loading indicator and feedback
    document.getElementById("loading").style.display = "flex";
    document.getElementById("sta").innerText = "Uploading, please wait...";
    document.getElementById("sta").style.color = "#03bcf4";

    // Simulate form submission for the upload process
    document.getElementById("upload").submit();
  } else {
    // Handle case where no file is selected
    document.getElementById("sta").innerText = "No file selected!";
    document.getElementById("sta").style.color = "red";
  }
});

// Function to confirm file removal
function rem() {
  // Display confirmation dialog
  if (confirm("Are you sure you want to remove this file?")) {
    console.log("File removal confirmed.");
    // Display feedback to user
    document.getElementById("sta").innerText = "Removing, please wait...";
    document.getElementById("sta").style.color = "#03bcf4";
    return true; // Proceed with the removal action (e.g., form submission)
  } else {
    // Handle case where user cancels the removal
    console.log("File removal canceled.");
    return false; // Prevent the action
  }
}









// function cho(){
//   document.getElementById("file").click();
// }

// document.getElementById("file").addEventListener("change",() =>{
//   document.getElementById("loading").style.display = "flex";
//   document.getElementById("sta").innerText = "Please wait...";
//   document.getElementById("sta").style.color = "#03bcf4";
//   document.getElementById("upload").submit();
// })

// function rem(){
//   if(confirm("Are you sure you want to Remove?")){
//       console.log("Removing");
//       document.getElementById("sta").innerText = "Please wait...";
//       document.getElementById("sta").style.color = "#03bcf4";
//       return true;
//   }
//   else{
//     console.log('no delete');
//     return false;
//   }
// }

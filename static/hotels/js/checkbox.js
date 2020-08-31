function myFunction() {
  // Get the checkbox
  var checks = document.querySelectorAll('[id^=myCheck]').length;
  for (j = 1; j < checks + 1; j++) {
    var checkBox = document.getElementById("myCheck" + j);
    // Get the output text
    var text = document.getElementById("text" + j);

    // If the checkbox is checked, display the output text
    if (checkBox.checked == true) {
      text.style.display = "block";
    } else {
      text.style.display = "none";
    }
  }
}

var prev = document.getElementById("previous_page");
prev.value = document.referrer;
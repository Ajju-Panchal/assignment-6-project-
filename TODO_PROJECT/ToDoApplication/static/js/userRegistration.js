$(document).ready(function() {
    $('#register-form').submit(function(event) {
      event.preventDefault(); // Prevent form submission

      // Validate fields
      var username = $('#username').val();
      var password = $('#password').val();
      var confirm_password = $("#password1").val();
      var email = $('#email').val();
      var mobileNumber = $('#phone').val();


      if (!username || !password || !confirm_password || !email || !phone) {
        alert('Please fill in all fields');
        return;
      }

      // Email validation
      var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        alert('Please enter a valid email address');
        return;
      }
      var mobileNumberRegex = /^[0-9]{10}$/;
      if (!mobileNumber.match(mobileNumberRegex)) {
        alert('Invalid mobile number. Please enter a 10-digit number.');
        return;
      }    
      if (password !== confirm_password){
        alert('Passwords do not match!!');
        return;
      }
      // Additional validation logic here

      // Submit the form if all validations pass
      this.submit();
    });
  });
$(document).ready(function() {
    $('#login-form').submit(function(event) {
      event.preventDefault(); // Prevent form submission

      // Validate fields
      var username = $('#username').val();
      var password = $('#password').val();

      if (!username || !password) {
        alert('Please fill in all fields');
        return;
      }

      // Additional validation logic here

      // Submit the form if all validations pass
      this.submit();
    });
  });
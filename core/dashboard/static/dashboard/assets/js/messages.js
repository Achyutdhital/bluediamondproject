// messages.js

$(document).ready(function() {
    $('#aboutForm').on('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this); // Create FormData object

        $.ajax({
            url: $(this).attr('action'), // Use form's action attribute
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // CSRF token
            },
            success: function(response) {
                console.log('AJAX Success:', response); // Log response
                if (response.success) {
                    $('#error-messages').html('<div class="alert alert-success">' + response.message + '</div>');
                    setTimeout(function() {
                        window.location.href = response.redirect_url || window.location.href; // Redirect if needed
                    }, 2000);
                } else {
                    var errors = JSON.parse(response.errors);
                    var errorMessages = '';
                    $.each(errors, function(field, messages) {
                        errorMessages += '<div class="alert alert-danger">' + messages + '</div>';
                    });
                    $('#error-messages').html(errorMessages);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', status, error); // Log errors
                $('#error-messages').html('<div class="alert alert-danger">An error occurred. Please try again.</div>');
            }
        });
    });

    // Helper function to get CSRF token from cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

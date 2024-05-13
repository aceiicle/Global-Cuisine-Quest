document.addEventListener('DOMContentLoaded', function() {
    // Example: Form Submission Feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input');
            inputs.forEach(input => {
                if (!input.value) {
                    e.preventDefault(); // Prevent form submission
                    input.classList.add('is-invalid'); // Add Bootstrap's is-invalid class for visual feedback
                    // Can also display a custom error message here
                }
            });
        });
    });

    // Initialize RateYo! for the difficulty level field
    var $rateYo = $(".rateyo").rateYo({
        fullStar: true
    });

    $rateYo.on("rateyo.set", function (e, data) {
        $('#difficulty_level').val(data.rating);
    });

    document.getElementById('loadMoreChallenges').addEventListener('click', function() {
        const request = new XMLHttpRequest();
        request.open('GET', '/your-endpoint-to-load-challenges', true);
        
        request.onload = function() {
            if (this.status >= 200 && this.status < 400) {
                // Success!
                const resp = this.response;
                document.getElementById('challengesContainer').innerHTML += resp; // Append new challenges
            } else {
                // We reached our target server, but it returned an error
            }
        };
        
        request.onerror = function() {
            // There was a connection error of some sort
        };
        
        request.send();
    });



});
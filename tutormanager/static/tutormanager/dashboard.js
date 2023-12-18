document.addEventListener('DOMContentLoaded', function() {

    var cancel_btn = document.querySelectorAll('.cancel-btn');
    if (cancel_btn != null ) {
        cancel_btn.forEach((btn) => {
            btn.addEventListener("click", () => cancel_schedule(btn));
        })
    }

})


function get_cookie(name) {
    if (!name) { return null; }
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length >= 2) return parts.pop().split(";").shift();
}


function cancel_schedule(btn) {
    var id = btn.getAttribute('data-id');

    fetch('/cancel_schedule/' + id, {
        method: 'POST',
        headers: {
            "X-CSRFToken": get_cookie("csrftoken"),
            "Content-Type": "application/json"
        },
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);

        if (result.error === undefined) {
            // Remove record from table
            row = document.querySelector('#lesson-'+id).remove();
        } else {
            alert(result.error);
        }
    });
}
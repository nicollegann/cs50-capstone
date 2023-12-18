document.addEventListener('DOMContentLoaded', function() {

    var remove_btn = document.querySelectorAll('.remove-btn');
    if (remove_btn != null ) {
        remove_btn.forEach((btn) => {
            btn.addEventListener("click", () => cancel_slot(btn));
        })
    }

})


function get_cookie(name) {
    if (!name) { return null; }
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length >= 2) return parts.pop().split(";").shift();
}


function cancel_slot(btn) {
    var id = btn.getAttribute('data-id');

    fetch('/delete_availability/' + id, {
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
            row = document.querySelector('#slot-'+id).remove();
        } else {
            alert(result.error);
        }
    });
}

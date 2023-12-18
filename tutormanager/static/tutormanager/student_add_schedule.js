document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('#success-notification').style.display = 'none';

    var select_btn = document.querySelectorAll('.select-btn');
    if (select_btn != null ) {
        select_btn.forEach((btn) => {
            btn.addEventListener("click", () => add_slot(btn));
        })
    }

})


function get_cookie(name) {
    if (!name) { return null; }
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length >= 2) return parts.pop().split(";").shift();
}


function add_slot(btn) {
    var id = btn.getAttribute('data-id');
    document.querySelector('#success-notification').style.display = 'none';

    fetch('/add_schedule/' + id, {
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

            notification = document.querySelector('#success-notification');
            notification.innerHTML = `Lesson scheduled on ${result.date}, ${result.time} successfully!`;
            notification.style.display = 'block';

        } else {
            alert(result.error);
        }
    });
}
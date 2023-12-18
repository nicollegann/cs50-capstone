document.addEventListener('DOMContentLoaded', function() {

    load_profile();

    var edit_btn = document.querySelector('#edit-btn')
    if (edit_btn != null) {
        edit_btn.addEventListener('click', edit_profile);
    }
})


function get_cookie(name) {
    if (!name) { return null; }
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length >= 2) return parts.pop().split(";").shift();
}


function load_profile() {
    // Show profile and hide edit view
    document.querySelector('#profile-view').style.display = 'block';
    document.querySelector('#edit-view').style.display = 'none';
}


function edit_profile() {
    id = document.querySelector('#edit-btn').getAttribute('data-id')

    // Fetch exisiting data
    fetch('/edit_profile/' + id)
    .then(response => response.json())
    .then(profile => {
        // Show edit form
        document.querySelector('#profile-view').style.display = 'none';
        document.querySelector('#edit-view').style.display = 'block';

        // Pre-fill fields
        document.querySelector('#first-name').value = profile.first_name;
        document.querySelector('#last-name').value = profile.last_name;
        document.querySelector('#academic-level').value = profile.acad_level;
        document.querySelector('#school').value = profile.school;

        document.querySelector('#edit-form').addEventListener('submit', submit_profile_update);
    })    
}


function submit_profile_update() {
    id = document.querySelector('#update-btn').getAttribute('data-id')

    console.log("fetched")

    fetch('/edit_profile/' + id, {
        method: 'POST',
        headers: {
            "X-CSRFToken": get_cookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            first_name: document.querySelector('#first-name').value,
            last_name:  document.querySelector('#last-name').value,
            acad_level: document.querySelector('#academic-level').value,
            school: document.querySelector('#school').value
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);

        if (result.error === undefined) {
            load_profile()
        } else {
            alert(result.error);
        }
    });
}
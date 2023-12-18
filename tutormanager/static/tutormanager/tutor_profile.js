document.addEventListener('DOMContentLoaded', function() {
    
    if (document.querySelector('#profile-view') !== null) {
        load_profile();
    }

    var edit_btn = document.querySelector('#edit-btn')
    if (edit_btn != null) {
        edit_btn.addEventListener('click', edit_profile);
    }

    var star_btn = document.querySelectorAll('.star-btn');
    if (star_btn != null ) {
        star_btn.forEach((btn) => {
            btn.addEventListener('click', () => star_handler(btn));
        })
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

function load_edit_form() {
    // Show profile and hide edit view
    document.querySelector('#profile-view').style.display = 'none';
    document.querySelector('#edit-view').style.display = 'block';
}


function edit_profile() {
    id = document.querySelector('#update-btn').getAttribute('data-id')

    // Fetch exisiting data
    fetch('/edit_profile/' + id)
    .then(response => response.json())
    .then(profile => {
        // Show edit form
        load_edit_form();

        // Pre-fill fields
        document.querySelector('#first-name').value = profile.first_name;
        document.querySelector('#last-name').value = profile.last_name;
        document.querySelector('#teaching-experience').value = profile.experience_years;
        document.querySelector('#bio').value = profile.bio;

        document.querySelector('#edit-form').addEventListener('submit', submit_profile_update);
    })    
}


function submit_profile_update() {
    id = document.querySelector('#edit-btn').getAttribute('data-id')

    fetch('/edit_profile/' + id, {
        method: 'POST',
        headers: {
            "X-CSRFToken": get_cookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            first_name: document.querySelector('#first-name').value,
            last_name:  document.querySelector('#last-name').value,
            experience_years: document.querySelector('#teaching-experience').value,
            bio: document.querySelector('#bio').value
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


function star_handler(btn) {
    var id = btn.getAttribute('data-id');
    var btn_state = btn.getAttribute('data-state');

    if (btn_state == 'unstar') {
        fetch('/star_profile/' + id, {
            method: 'POST',
            headers: {
                "X-CSRFToken": get_cookie("csrftoken"),
                "Content-Type": "application/json"
            }}
        )
        .then(response => response.json())
        .then(result => {
            console.log(result)

            btn.classList.remove('fa-regular');
            btn.classList.add('fa-solid');
            btn.setAttribute('data-state', 'star'); 

            document.querySelector(`#star-count-${id}`).innerHTML = result.star_count;

        }).catch(() => {
            alert('Please login first!')
        })
        
    } else if (btn_state == 'star') {
        fetch('/unstar_profile/' + id, {
            method: 'POST',
            headers: {
                "X-CSRFToken": get_cookie("csrftoken"),
                "Content-Type": "application/json"
            }}
        )
        .then(response => response.json())
        .then(result => {
            console.log(result)

            btn.classList.remove('fa-solid');
            btn.classList.add('fa-regular');
            btn.setAttribute('data-state', 'unstar');

            document.querySelector(`#star-count-${id}`).innerHTML = result.star_count;
        }).catch(() => {
            alert('Please login first!')
        })
    }
}


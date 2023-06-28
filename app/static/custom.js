function changeOwnerShow(show_id) {
    spinner.removeAttribute('hidden');
    fetch("/tv_show/"+show_id+"/change_owner", {
        headers: {
            'Content-Type': 'application/json'
        },
        method : 'POST',
        signal: AbortSignal.timeout(5_000)
    })
    .then(function (response){
        spinner.setAttribute('hidden', '');
        if (response.ok) {
            response.json()
            .then(function(response) {
                toastr.success(response.message)
            })
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

function changeOwnerMovie(movie_id) {
    spinner.removeAttribute('hidden');
    fetch("/movies/"+movie_id+"/change_owner", {
        headers: {
            'Content-Type': 'application/json'
        },
        method : 'POST',
        signal: AbortSignal.timeout(5_000)
    })
    .then(function (response){
        spinner.setAttribute('hidden', '');
        if (response.ok) {
            response.json()
            .then(function(response) {
                toastr.success(response.message)
            })
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}
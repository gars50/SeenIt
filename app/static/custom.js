function changeOwnerMovie(movie_id, object) {
    spinner.removeAttribute('hidden');
    var row = object.parentNode.parentNode
    fetch("/media/movie/"+movie_id+"/change_owner", {
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
            row.parentNode.removeChild(row)
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

function changeOwnerShow(show_id, object) {
    spinner.removeAttribute('hidden');
    var row = object.parentNode.parentNode
    fetch("/media/tv_show/"+show_id+"/change_owner", {
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
            row.parentNode.removeChild(row)
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

function deleteMovie(movie_id, object) {
    spinner.removeAttribute('hidden')
    var row = object.parentNode.parentNode
    fetch("/media/movie/"+movie_id+"/delete", {
        headers: {
            'Content-Type': 'application/json'
        },
        method : 'DELETE',
        signal: AbortSignal.timeout(5_000)
    })
    .then(function (response){
        spinner.setAttribute('hidden', '');
        if (response.ok) {
            response.json()
            .then(function(response) {
                toastr.success(response.message)
            })
            row.parentNode.removeChild(row)
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

function deleteShow(show_id, object) {
    spinner.removeAttribute('hidden')
    var row = object.parentNode.parentNode
    fetch("/media/tv_show/"+show_id+"/delete", {
        headers: {
            'Content-Type': 'application/json'
        },
        method : 'DELETE',
        signal: AbortSignal.timeout(5_000)
    })
    .then(function (response){
        spinner.setAttribute('hidden', '');
        if (response.ok) {
            response.json()
            .then(function(response) {
                toastr.success(response.message)
            })
            row.parentNode.removeChild(row)
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

$(document).ready(function(){
    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
            $(this).toggle($(this).find('th').text().toLowerCase().indexOf(value) > -1)
        });
    });
});
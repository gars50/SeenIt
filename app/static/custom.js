function fetchToastRemoveRow(url, obj, type) {
    var row = obj.parentNode.parentNode
    var table = $('#mediaTable').DataTable();
    spinner.removeAttribute('hidden');
    fetch(url, {
        headers: {
            'Content-Type': 'application/json'
        },
        method : type,
        signal: AbortSignal.timeout(5_000)
    })
    .then(function (response){
        spinner.setAttribute('hidden', '');
        if (response.ok) {
            response.json()
            .then(function(response) {
                toastr.success(response.message)
            })
            table.row(row).remove().draw()
        } else {
            response.json()
            .then(function(response) {
                toastr.error(response.message)
            })
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

function changeOwnerMovie(movie_id, obj) {
    var fetchURL = "/media/movie/"+movie_id+"/change_owner"
    fetchToastRemoveRow(fetchURL, obj, 'POST')
}

function changeOwnerShow(show_id, obj) {
    var fetchURL = "/media/tv_show/"+show_id+"/change_owner"
    fetchToastRemoveRow(fetchURL, obj, 'POST')
}

function deleteMovie(movie_id, obj) {
    var fetchURL = "/media/movie/"+movie_id+"/delete"
    fetchToastRemoveRow(fetchURL, obj, 'DELETE')
}

function deleteShow(show_id, obj) {
    var fetchURL = "/media/tv_show/"+show_id+"/delete"
    fetchToastRemoveRow(fetchURL, obj, 'DELETE')
}

$(document).ready(function () {
    $('#mediaTable').DataTable({
        "lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "All"] ],
        "columnDefs": [{
            "targets": 'nosort',
            "orderable": false,
            "width": "5%"
        }]
    });
  });

  toastr.options = {
    closeButton: true,
    progressBar: true
  }
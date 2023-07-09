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
                toastr.error(response.error)
            })
        }
    })
    .catch(function(error) {
        console.log(error)
    })
}

function addPick(media_id, obj) {
    var fetchURL = "/media/"+media_id+"/add_pick"
    fetchToastRemoveRow(fetchURL, obj, 'POST')
}

function deletePick(pick_id, obj) {
    var fetchURL = "/media/pick/"+pick_id+"/delete"
    fetchToastRemoveRow(fetchURL, obj, 'DELETE')
}

function deleteMedia(media_id, obj) {
    var fetchURL = "/media/"+media_id+"/delete"
    fetchToastRemoveRow(fetchURL, obj, 'DELETE')
}

$(document).ready(function () {
    $('#mediaTable').DataTable({
        "lengthMenu": [ [10, 25, 50, -1], [10, 25, 50, "All"] ],
        "columnDefs": [{
            "targets": 'nosort',
            "orderable": false,
            "width": "7%"
        }]
    });
  });

toastr.options = {
    closeButton: true,
    progressBar: true
  }
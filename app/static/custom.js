function fetchToastRemoveRowMediaTable(url, obj, type) {
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
            table.row(row).remove().draw(false)
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

function fetchToastRemoveRowTable(url, obj, type) {
    var row = obj.parentNode.parentNode
    var rowIndex = row.rowIndex
    var table = row.parentNode.parentNode
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
            table.deleteRow(rowIndex);
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

function deletePickModal(pick_id, obj) {
    var fetchURL = BASE_URL+"/media/pick/"+pick_id+"/delete"
    fetchToastRemoveRowTable(fetchURL, obj, 'DELETE')
}

function addPick(media_id, obj) {
    var fetchURL = BASE_URL+"/media/"+media_id+"/add_pick"
    fetchToastRemoveRowMediaTable(fetchURL, obj, 'POST')
}

function deletePick(pick_id, obj) {
    var fetchURL = BASE_URL+"/media/pick/"+pick_id+"/delete"
    fetchToastRemoveRowMediaTable(fetchURL, obj, 'DELETE')
}

function deleteMedia(media_id, obj) {
    var fetchURL = BASE_URL+"/media/"+media_id+"/delete"
    var result = confirm("Are you sure you want to delete this media : "+obj.parentNode.parentNode.firstChild.nextElementSibling.innerText)
    if (result) {
        fetchToastRemoveRowMediaTable(fetchURL, obj, 'DELETE')
    }
}

function modalPicks(media_id, obj) {
    var fetchURL = BASE_URL+"media/"+media_id+"/picks_modal"
    $.ajax(fetchURL, {
        method: 'GET',
        dataType: 'html',
        success: function(data) {
            var mediaTitle = obj.parentNode.parentNode.childNodes[1].innerText
            $("#picksTitle").text("Picks for "+mediaTitle)
            $("#picksBody").html(data);
        }
    });
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
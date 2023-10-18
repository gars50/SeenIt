function fetchToastRemoveRowDataTable(url, obj, type) {
    var row = obj.parentNode.parentNode
    var table = $(obj.closest('.table')).DataTable();
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

function appendPickPermanent(media_id, obj) {
    var fetchURL = BASE_URL+"/api/picks/"+media_id+"/add_permanent"
    fetchToastRemoveRowTable(fetchURL, obj, 'PUT')
}

function appendPickCurrentUser(media_id, obj) {
    var fetchURL = BASE_URL+"/api/picks/"+media_id+"/add_to_current_user"
    fetchToastRemoveRowTable(fetchURL, obj, 'PUT')
}

function deletePickModal(pick_id, obj) {
    var fetchURL = BASE_URL+"/api/picks/"+pick_id+"/delete"
    fetchToastRemoveRowTable(fetchURL, obj, 'DELETE')
}

function addPickCurrentUser(media_id, obj) {
    var fetchURL = BASE_URL+"/api/picks/"+media_id+"/add_to_current_user"
    fetchToastRemoveRowDataTable(fetchURL, obj, 'PUT')
}

function addPickPermanent(media_id, obj) {
    var fetchURL = BASE_URL+"/api/picks/"+media_id+"/add_permanent"
    fetchToastRemoveRowDataTable(fetchURL, obj, 'PUT')
}

function deletePick(pick_id, obj) {
    var fetchURL = BASE_URL+"/api/picks/"+pick_id+"/delete"
    fetchToastRemoveRowDataTable(fetchURL, obj, 'DELETE')
}

function deleteMedia(media_id, obj) {
    var fetchURL = BASE_URL+"/api/medias/"+media_id+"/delete"
    var result = confirm("Are you sure you want to delete this media : "+obj.parentNode.parentNode.firstChild.nextElementSibling.innerText)
    if (result) {
        fetchToastRemoveRowDataTable(fetchURL, obj, 'DELETE')
    }
}

function modalPicks(media_id, obj) {
    var fetchURL = BASE_URL+"/api/medias/"+media_id+"/picks_modal"
    $.ajax(fetchURL, {
        method: 'GET',
        dataType: 'html',
        success: function(data) {
            $("#picksBody").html(data);
            flask_moment_render_all();
        }
    });
}

toastr.options = {
    closeButton: true,
    progressBar: true
}

function formatBytes(bytes, decimals = 2) {
    if (!+bytes) return '0 Bytes'

    const k = 1024
    const dm = decimals < 0 ? 0 : decimals
    const sizes = ['Bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']

    const i = Math.floor(Math.log(bytes) / Math.log(k))

    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`
}
$(document).ready(uploadList);

function uploadList() {
    console.log("upload file list here");
    $('#table-upload-processing').show();
    fetch(getRequest())
        .then(getResponse)
        .then(updateFilesList)
        .catch(errorHandler)
        .finally(finallyAction)
}

function finallyAction() {
    $('#table-upload-processing').hide();
}

function getRequest() {
    let url = '/crawler/files';
    return new Request(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json',
                   'Cache-Control': 'no-cache, no-store, must-revalidate'},
    });
}

function getResponse(response) {
    if (!response.ok) throw response;
    return response.json();
}

function errorHandler(error) {
    alert(error);
}

function clearTable() {
    let table = document.getElementById("file-list-table");
    table.innerHTML = ''
}

function updateFilesList(json) {
    function makeTableRow(row) {
        function create_th(text) {
            let th = document.createElement("th");
            th.appendChild(document.createTextNode(text));
            return th
        }

        function create_td(text, reference_flag=false, reference_link='') {
            let td = document.createElement("td");
            if (reference_flag) {
                let a = document.createElement('a');
                a.href = reference_link;
                a.innerHTML = text;
                td.appendChild(a);
            } else {
                td.appendChild(document.createTextNode(text));
            }
            return td
        }

        let tr = document.createElement("tr");
        tr.appendChild(create_th(row.id));
        tr.appendChild(create_td(row.name, true, "/crawler/fileview/" + row.id));
        tr.appendChild(create_td(row.time));
        tr.appendChild(create_td(row.urls_count));
        return tr
    }

    clearTable();
    let json_data = JSON.parse(json);
    for (let row of json_data)
    {
        document.getElementById("file-list-table").appendChild(makeTableRow(row));
    }
}

function uploadFile(button) {
    function getFormData() {
        let fd = new FormData();
        let file_input = document.getElementById('pdf-file-input');
        let csrf_token_input = document.getElementsByName("csrfmiddlewaretoken")[0];
        fd.append(file_input.name, file_input.files[0]);
        fd.append(csrf_token_input.name, csrf_token_input.value);
        return fd
    }

    function disableButton(flag=true) {
        console.log(button);
        if (flag) {
            button.disabled = true;
            $('#file-upload-processing').show();
        } else {
            button.disabled = false;
            $('#file-upload-processing').hide();
        }
    }

    function initialXHR() {
        let xhr = new XMLHttpRequest();

        xhr.onload = function() {
            if (this.status == 200) {
                uploadList();
            } else {
                alert('Error request');
            }
            document.getElementById('pdf-file-input').value='';
            disableButton(false);
        };
        return xhr
    }

    disableButton();
    let xhr = initialXHR();
    xhr.open("POST", "/crawler/files/", true);
    xhr.send(getFormData());
}

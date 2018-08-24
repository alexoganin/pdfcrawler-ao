$(document).ready(uploadFileData);

function uploadFileData() {
    console.log("Upload file data here");
    fetch(getRequest())
        .then(getResponse)
        .then(updateFileData)
        .catch(errorHandler)
}

function getRequest() {
    let url = '/crawler/files/'+$('#file-id').val();
    return new Request(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json',
                   'Cache-Control': 'no-cache, no-store, must-revalidate'},
    })
}

function updateFileData(data) {
    function updateFileDescription(json_data) {
        document.getElementById('file-name').innerHTML = json_data.name;
        document.getElementById('file-url-count').innerHTML = json_data.urls_count;
        document.getElementById('file-created-time').innerHTML = json_data.time;
    }

    function updateUrlList(json_urls) {
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
            tr.appendChild(create_td(row.path, true, "/crawler/urlview/"+row.id));
            tr.appendChild(create_td(row.http_code));
            tr.appendChild(create_td(row.alive));
            return tr
        }


        for (let row of json_urls) {
            console.log(row);
            document.getElementById('url-list-table').appendChild(makeTableRow(row))
        }
    }

    let json_data = JSON.parse(data);
    updateFileDescription(json_data);
    updateUrlList(json_data.urls)
}

function getResponse(response) {
    if (!response.ok) throw response;
    return response.json();
}

function errorHandler(error) {
    alert(error);
}
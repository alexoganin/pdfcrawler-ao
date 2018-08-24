$(document).ready(uploadUrlData);

function uploadUrlData() {
    fetch(getRequest())
        .then(getResponse)
        .then(updateUrlData)
        .catch(errorHandler)
}

function getRequest() {
    let url = '/crawler/urls/'+ $('#url-id').val();
    return new Request(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json',
                   'Cache-Control': 'no-cache, no-store, must-revalidate'},
    })
}

function getResponse(response) {
    if (!response.ok) throw response;
    return response.json();
}

function errorHandler(error) {
    alert(error);
}

function updateUrlData(data) {

    function updateUrlDescription(json_data) {
        document.getElementById('url-path').innerHTML=json_data.path;
        document.getElementById('url-http-code').innerHTML=json_data.http_code;
        document.getElementById('url-alive').innerHTML=json_data.alive
    }

    function updateFileList(files) {
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
            tr.appendChild(create_td(row.name, true, "/crawler/fileview/"+row.id));
            tr.appendChild(create_td(row.time));
            return tr
        }


        for (let row of files) {
            console.log(row);
            document.getElementById('file-list-table').appendChild(makeTableRow(row))
        }
    }

    let json_data = JSON.parse(data);
    console.log(json_data);
    updateUrlDescription(json_data);
    updateFileList(json_data.files)
}

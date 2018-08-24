$(document).ready(uploadUrlList);

function uploadUrlList() {
    fetch(getRequest())
        .then(getResponse)
        .then(updateUrlList)
        .catch(errorHandler)
}

function getRequest() {
    let url = '/crawler/urls';
    return new Request(url, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json',
                   'Cache-Control': 'no-cache, no-store, must-revalidate'},
    });
}

function errorHandler(error) {
    alert(error);
}

function getResponse(response) {
    if (!response.ok) throw response;
    return response.json();
}

function clearTable() {
    let table = document.getElementById("url-list-table");
    table.innerHTML = ''
}

function updateUrlList(data) {
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

    let json_urls = JSON.parse(data);
    for (let row of json_urls) {
        document.getElementById('url-list-table').appendChild(makeTableRow(row))
    }
}
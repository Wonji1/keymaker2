
function createQRDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'create_qr') {
        var url = $("#create_qr_url").val();
        var name = $("#create_qr_name").val();
        postData = {url : url, name : name};
        uri = baseURL + 'api/create_qr/' + url + '/' + name;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

/*
function readQRDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'read_qr') {
        var file = $("#read_qr_file").val();
        postData = {file : file};
        uri = baseURL + 'api/read_qr/' + file ;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}
*/

function issueKeyDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'issue_key') {
        var user_key = $("#issue_key_user_key").val();
        var index = $("#issue_key_index").val();
        var user_ip = $("#issue_key_user_ip").val();
        var qr_key = $("#issue_key_qr_key").val();
        var version = $("#issue_key_version").val();
        var memo = $("#issue_key_memo").val();
        postData = {user_key : user_key, index : index, user_ip : user_ip, qr_key : qr_key, version : version, memo : memo};
        uri = baseURL + 'api/issue_key/' + user_key + '/' + index + '/' + user_ip + '/' + qr_key + "/" + version + "/" + memo;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function getKeyListDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'get_key_list') {
        var user_key = $("#get_key_list_user_key").val();
        var user_name = $("#get_key_list_user_name").val();
        var address = $("#get_key_list_address").val();
        var user_id = $("#get_key_list_user_id").val();
        var date_start = $("#get_key_list_date_start").val();
        var date_end = $("#get_key_list_date_end").val();
        var currentpage = $("#get_key_list_currentpage").val();
        var countperpage = $("#get_key_list_countperpage").val();

        postData = {user_key : user_key, user_name : user_name, address : address, user_id : user_id,
                    date_start : date_start, date_end : date_end, currentpage : currentpage, countperpage : countperpage};
        uri = baseURL + 'api/get_key_list/' + user_key + '/' + user_name + "/" + address + "/" + user_id + "/"
                                            + date_start + "/" + date_end + "/" + currentpage + "/" + countperpage;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function getKeyInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'get_key_info') {
        var user_key = $("#get_key_info_user_key").val();
        var index = $("#get_key_info_index").val();

        postData = {user_key : user_key, index : index};
        uri = baseURL + 'api/get_key_info/' + user_key + '/' + index;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}


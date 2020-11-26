
function addModInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'add_module_info') {
        var user_key = $("#add_module_info_user_key").val();
        var module_name = $("#add_module_info_module_name").val();
        var version = $("#add_module_info_version").val();
        var memo = $("#add_module_info_memo").val();

        postData = {user_key : user_key, module_name : module_name, version : version, memo : memo};
        uri = baseURL + 'api/add_module_info/' + user_key + '/' + module_name + '/' + version + '/' + memo;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function getModListDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'get_module_list') {
        var user_key = $("#get_module_list_user_key").val();
        var module_name = $("#get_module_list_module_name").val();
        var user_name = $("#get_module_list_user_name").val();
        var version = $("#get_module_list_version").val();
        var memo = $("#get_module_list_memo").val();
        var date_reg_start = $("#get_module_list_date_reg_start").val();
        var date_reg_end = $("#get_module_list_date_reg_end").val();
        var currentpage = $("#get_module_list_currentpage").val();
        var countperpage = $("#get_module_list_countperpage").val();

        postData = {user_key : user_key, module_name : module_name, user_name : user_name, version : version,
                    memo : memo, date_reg_start : date_reg_start, date_reg_end : date_reg_end, currentpage : currentpage,
                    countperpage : countperpage};
        uri = baseURL + 'api/get_module_list/' + user_key + '/' + module_name + '/' + user_name + '/'
                                                + version + '/' + memo + '/' + date_reg_start + '/'
                                                + date_reg_end + '/' + currentpage + '/' + countperpage;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function getModInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'get_module_info') {
        var user_key = $("#get_module_info_user_key").val();
        var request = $("#get_module_info_request").val();
        var module_index = $("#get_module_info_module_index").val();

        postData = {user_key : user_key, request : request, module_index : module_index};
        uri = baseURL + 'api/get_module_info/' + user_key + '/' + request + '/' + module_index;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function setModInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'set_module_info') {
        var user_key = $("#set_module_info_user_key").val();
        var module_index = $("#set_module_info_module_index").val();
        var module_name = $("#set_module_info_module_name").val();
        var version = $("#set_module_info_version").val();
        var memo = $("#set_module_info_memo").val();

        postData = {user_key : user_key, module_index : module_index, module_name : module_name, version : version, memo : memo};
        uri = baseURL + 'api/set_module_info/' + user_key + '/' + module_index + '/' + module_name + '/' + version + '/' + memo;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function delModInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'del_module_info') {
        var user_key = $("#del_module_info_user_key").val();
        var module_index = $("#del_module_info_module_index").val();
        var file_exist_flag = $("#del_module_info_file_exist_flag").val();

        postData = {user_key : user_key, module_index : module_index, file_exist_flag : file_exist_flag};
        uri = baseURL + 'api/del_module_info/' + user_key + '/' + module_index + '/' + file_exist_flag;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function delFileDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'del_file') {
        var user_key = $("#del_file_user_key").val();
        var request = $("#del_file_request").val();
        var index = $("#del_file_index").val();

        postData = {user_key : user_key, request : request, index : index};
        uri = baseURL + 'api/del_file/' + user_key + '/' + request + '/' + index;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function downModDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'down_module') {
        var user_key = $("#down_module_user_key").val();
        var index = $("#down_module_index").val();

        postData = {user_key : user_key, index : index};
        uri = baseURL + 'api/down_module/' + user_key + '/' + index;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}


function loginDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'login') {
        var id = $("#login_user_id").val();
        var pw = $("#login_user_pw").val();
        postData = {user_id : id, user_pw : pw};
        uri = baseURL + 'api/login/' + id + '/' + pw;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function logoutDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'logout') {
        var ip = $("#logout_user_ip").val();
        postData = {user_ip: ip};
        uri = baseURL + 'api/logout/' + ip;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function getUserInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'get_user_info') {
        var key = $("#get_user_info_user_key").val();
        var id = $("#get_user_info_user_id").val();
        var req = $("#get_user_info_request").val();

        postData = {user_key : key, user_id : id, request : req};
        uri = baseURL + 'api/get_user_info/' + key + '/' + id + '/' +  req;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function addUserInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'add_user_info') {
        var id = $("#add_user_info_user_id").val();
        var pw = $("#add_user_info_user_pw").val();
        var user_name = $("#add_user_info_user_name").val();
        var company_name = $("#add_user_info_company_name").val();
        var department = $("#add_user_info_department").val();
        var position = $("#add_user_info_user_position").val();
        var phone_number = $("#add_user_info_phone_number").val();
        var email = $("#add_user_info_email").val();

        postData = {user_id : id, user_pw : pw, user_name : user_name,
                    company_name : company_name, department : department,
                    position : position, phone_number : phone_number, email : email};

        uri = baseURL + 'api/add_user_info/' + id + '/' + pw + '/' + user_name + '/'
                                             + company_name + '/' + department + '/' + position
                                             + '/' + phone_number + '/' + email;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function setUserInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'set_user_info') {
        var id = $("#set_user_info_user_key").val();
        var request = $("#set_user_info_request").val();
        var pw = $("#set_user_info_user_pw").val();
        var user_name = $("#set_user_info_user_name").val();
        var company_name = $("#set_user_info_company_name").val();
        var department = $("#set_user_info_department").val();
        var position = $("#set_user_info_position").val();
        var phone_number = $("#set_user_info_phone_number").val();
        var email = $("#set_user_info_email").val();

        postData = {user_id : id, request : request, user_pw : pw, user_name : user_name,
                    company_name : company_name, department : department,
                    position : position, phone_number : phone_number, email : email};

        uri = baseURL + 'api/set_user_info/' + id + '/' + request + '/' + pw + '/' + user_name + '/'
                                             + company_name + '/' + department + '/' + position + '/'
                                             + phone_number + '/' + email;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function getAccessInfoDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'get_access_info') {
        var user_key = $("#get_access_info_user_key").val();

        postData = {user_key : user_key};

        uri = baseURL + 'api/get_access_info/' + user_key;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function setUserWihDelFlagDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'set_user_wih_del_flag') {
        var user_key = $("#set_user_wih_del_flag_user_key").val();
        var request = $("#set_user_wih_del_flag_request").val();

        postData = {user_key : user_key, request : request};

        uri = baseURL + 'api/set_user_wih_del_flag/' + user_key + '/' + request;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function getUserAuthDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'get_user_auth') {
        var user_key = $("#get_user_auth_user_key").val();

        postData = {user_key : user_key};

        uri = baseURL + 'api/get_user_auth/' + user_key;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}
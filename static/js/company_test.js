
function getComListDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'get_company_list') {
        var user_key = $("#get_company_list_user_key").val();
        var name = $("#get_company_list_name").val();
        var currentpage = $("#get_company_list_currentpage").val();
        var countperpage = $("#get_company_list_countperpage").val();

        postData = {get_company_list_user_key : user_key,
                    get_company_list_name : name,
                    get_company_list_currentpage : currentpage,
                    get_company_list_countperpage : countperpage};

        uri = baseURL + 'api/get_company_list/' + user_key + '/' + name + '/' + currentpage + '/' + countperpage;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}

function addComListDivProcess(type, showResultPId, isget) {
    var uri = '';
    var isJson = false;
    var arrData = null;
    var postData = null;

    if (type == 'add_company_list') {
        var user_key = $("#add_company_list_user_key").val();
        var com_name = $("#add_company_list_com_name").val();
        var com_address = $("#add_company_list_com_address").val();
        var phone_number = $("#add_company_list_user_phone_number").val();
        var email = $("#add_company_list_email").val();
        var memo = $("#add_company_list_memo").val();
        var day_max_count = $("#add_company_list_day_max_count").val();
        var max_count = $("#add_company_list_max_count").val();
        var date_max = $("#add_company_list_date_max").val();

        postData = {add_company_list_user_key : user_key,
                    add_company_list_com_name : com_name,
                    add_company_list_com_address : com_address,
                    add_company_list_user_phone_number : phone_number,
                    add_company_list_email : email,
                    add_company_list_memo : memo,
                    add_company_list_day_max_count : day_max_count,
                    add_company_list_max_count : max_count,
                    add_company_list_date_max : date_max};

        uri = baseURL + 'api/add_company_list/' + user_key + '/' + com_name + '/' + com_address + '/'
                                                + phone_number + '/' + email + '/' + memo + '/'
                                                + day_max_count + '/' + max_count + '/' + date_max;
    }

    if(isJson) {
        sendJsonAjax(uri, showResultPId, isget, arrData);
    } else {
        sendAjax(uri, showResultPId, isget, postData);
    }
}
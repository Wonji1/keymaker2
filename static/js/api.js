var baseURL = "http://" + apiAddress + "/";

$(document).ready(function(){
    url = "http://" + apiAddress + "/loginTest";
    $("#context_10000").load(url);

    $('#code_select').change(function () {
        url = "";
        if ($(this).val() == 'login_div') {
            url = "http://" + apiAddress + "/loginTest";
        }
        else if ($(this).val() === 'company_div') {
            url = "http://" + apiAddress + "/companyTest";
        } else if ($(this).val() === 'module_div') {
            url = "http://" + apiAddress + "/moduleTest";
        } else if ($(this).val() === 'key_div') {
            url = "http://" + apiAddress + "/keyTest";
        }

        if (url != "") {
        $("#context_10000").load(url);
        }
    });

});

// API 실행 함수
// type : 실행할 API 명
// showResultPId : API 결과값이 보여질 <p> 태그의 ID
function testFunction(type, showResultPId, isget, highRankDiv_id) {
    // login_test
    if (highRankDiv_id == "login_div") {
        loginDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'logout_div') {
        logoutDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'get_user_info_div') {
        getUserInfoDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'add_user_info_div') {
        addUserInfoDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'set_user_info_div') {
        setUserInfoDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'get_access_info_div') {
        getAccessInfoDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'set_user_wih_del_flag_div') {
        setUserWihDelFlagDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'get_user_auth_div') {
        getUserAuthDivProcess(type, showResultPId, isget);
    }


    // company_test
    else if (highRankDiv_id == 'get_company_list_div') {
        getComListDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'add_company_list_div') {
        addComListDivProcess(type, showResultPId, isget);
    }

    // module_test
    else if (highRankDiv_id == 'add_module_info_div') {
        addModInfoDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'get_module_list_div') {
        getModListDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'get_module_info_div') {
        getModInfoDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'set_module_info_div') {
        setModInfoDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'del_module_info_div') {
        delModInfoDivProcess(type, showResultPId, isget);
    }
    // upload_file 는 폼 제출 형식으로 따로 함수가 존재하지 않음
     else if (highRankDiv_id == 'del_file_div') {
        delFileDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'down_module_div') {
        downModDivProcess(type, showResultPId, isget);
    }

    // key_test
    else if (highRankDiv_id == 'create_qr_div') {
        createQRDivProcess(type, showResultPId, isget);
    }
    /*
    else if (highRankDiv_id == 'read_qr_div') {
        readQRDivProcess(type, showResultPId, isget);
    }
    */
    // read_qr 은 폼 제출 형식으로 따로 함수가 존재하지 않음
    else if (highRankDiv_id == 'issue_key_div') {
        issueKeyDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'get_key_list_div') {
        getKeyListDivProcess(type, showResultPId, isget);
    } else if (highRankDiv_id == 'get_key_info_div') {
        getKeyInfoDivProcess(type, showResultPId, isget);
    }
}

function sendAjax(url, showResultPId, isget, postData) {
    var ajaxType = 'post';

    if(isget == 'true') {
        postData = null;
        ajaxType = 'get';
    }

    $.ajax({
        url: url,
        type: ajaxType,
        data: postData,
        async: false,
        crossOrigin: true,
        cache: false,
        success: function(msg) {
            $("#" + showResultPId).text(JSON.stringify(msg))
        },
        error: function(jpXHR, textStatus, errorThrown) {
            var msg = '';
            if (jqXHR.status === 0) {
                msg = 'Not connect.\n Verify Network.';
            } else if (jqXHR.status == 404) {
                msg = 'Requested page not found. [404]';
            } else if (jqXHR.status == 500) {
                msg = 'Internal Server Error [500].';
            } else if (exception === 'parsererror') {
                msg = 'Requested JSON parse failed.';
            } else if (exception === 'timeout') {
                msg = 'Time out error.';
            } else if (exception === 'abort') {
                msg = 'Ajax request aborted.';
            } else {
                msg = 'Uncaught Error.\n' + jqXHR.responseText;
            }
            // 해당 URL에 뿌려놓은 text들을 저장
            $("#" + showResultPId).text(JSON.stringify(msg));
        }
    });
}

// API 단위 별로 버튼을 누르면 보여졌다가 가리거나 함
function hideShowFunction(div_id, input_id) {
    if ($("#" + div_id).css("display") == "none") {
        $("#" + div_id).show();
        $("#" + input_id).val("접기");
    } else {
        $("#" + div_id).hide();
        $("#" + input_id).val("펼치기");
    }
}

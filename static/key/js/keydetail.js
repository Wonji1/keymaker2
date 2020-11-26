//20200623 wonjihoon 인증키 상세 조회하는 파일

//20200601 wonjihoon 인증키 상세 팝업정보
//20200602 wonjihoon 인증키 조회 권한 없을 시 이전 페이지 이동

document.write("<script src='/static/main/js/config.js'></script>");

//20200601 wonjihoon 인증키 상세 팝업정보
//20200602 wonjihoon 인증키 조회 권한 없을 시 이전 페이지 이동
$(document).ready(function(){
    if(SValue != null){
    if(SValue.AUTH.indexOf('AUKEY0003') == -1){history.back(); alert('인식키 조회 권한이 존재하지 않습니다. 이전 페이지로 이동합니다.')}}
    if (SValue == null) {
        alert('로그인을 진행해 주세요.');
        location.href = '/login'}// SValue --> config.js 파일에 있으며 session에 저장된 key에 대한 value 값이다 , AUKEY0003은 인식키 조회 권한이다.
    $.ajax({
        url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/get_key_info/' + SKey +'/'+ document.getElementById("idx").value,
        type: 'post',
        success: function (data) {
            if(data.status == '400'){alert('접속해있는 사용자가 아닙니다.'); return}
            if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
            if(data.status == '402'){alert('인식키 상세정보 조회 도중 DB 에러가 났습니다.'); return}
            if(data.status == '403'){alert('입력값에서 DB 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.'); return}
            if(data.status == '404'){alert('인식키 조회 권한이 존재하지 않습니다.'); return}

            $("#user_name").html(data.data[0].USER_NAME);
            $("#user_id").html(data.data[0].result_data_1);
            $("#user_comp").html(data.data[0].COMPANY_NAME);
            $("#user_rank").html(data.data[0].POSITION);
            $("#user_mail").html(data.data[0].EMAIL);
            $("#user_service").html(data.data[0].LOGIN);
            $("#user_phone").html(data.data[0].PHONE_NUMBER);

            $("#key_val").html(data.data[0].ISSUE_KEY);
            $("#key_place").html(data.data[0].FULL_ADDRESS);
            $("#key_date").html(data.data[0].DATE + ' ' + data.data[0].TIME);
            $("#key_memo").html(data.data[0].MEMO);

        },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            return
        }
    });

});
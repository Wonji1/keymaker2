//20200623 wonjihoon 로그인 파일

//20200514 wonjihoon 로그인화면 이동 시 세션 초기화
//20200508 wonjihoon 로그인 기능
//20200508 wonjihoon 로그인 버튼
//20200508 wonjihoon 회원가입 페이지 이동 버튼

document.write("<script src='/static/main/js/config.js'></script>");

//20200514 wonjihoon 로그인화면 이동 시 세션 초기화
$(document).ready(function(){
    if(SKey != null){//SKey --> config.js 파일에 있으며 session에 저장된 key
                alert('로그인 정보가 초기화 되었습니다. 다시 로그인하여 주세요.');
                $.ajax({
                    url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/ip',
                    type: 'get',

                    success: function(data) {
                        $.ajax({
                            url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/logout/'+data,
                            type: 'post',
                            success: function (data) {
                                if(data.status == '400'){alert('IP 추출이 제대로 적용되지 않았습니다.'); return}
                                if(data.status == '401'){alert('동일한 IP로 접속한 사용자가 없습니다.'); return}
                                if(data.status == '402'){alert('동일한 IP로 접속한 사용자 조회 시 DB 에러가 났습니다.'); return}
                            },
                            error:function(request,status,error){
                                alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                                return
                            }
                        });
                    },
                    error:function(request,status,error){
                        alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                        return
                    }

                });
        sessionStorage.clear();
    }
});

//20200508 wonjihoon 로그인 기능
function getLogInfo() {

    var user_id = document.getElementById("user_id").value;
    user_id = user_id.toLowerCase();
    var user_pw = document.getElementById("user_pw1").value;
    user_pw = user_pw.toLowerCase();

    if (user_id == "" || user_pw == "") {
        alert("입력창이 비었습니다.");
        return
    }
    if(check_db.test(user_id) || check_db.test(user_pw)){
        alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
        return
    }
    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/login/'+user_id+'/'+ user_pw,
        type: 'post',
        success: function (data) {
            if(data.status == '400'){alert('ID에 영어, 숫자 이외의 문자가 존재합니다.'); return}
            if(data.status == '401'){alert('PW에 영어, 숫자 이외의 문자가 존재합니다.'); return}
            if(data.status == '402'){alert('IP 추출이 제대로 적용되지 않았습니다.'); return}
            if(data.status == '403'){alert('로그아웃 API가 호출되었으나 동일한 IP가 조회되지 않았습니다.'); return}
            if(data.status == '404'){alert('로그아웃 API가 호출되었으나 DB 조회 시 에러가 났습니다.'); return}
            if(data.status == '405'){alert('동일한 IP로 접속한 사용자가 있어 로그아웃 되었습니다.'); return}
            if(data.status == '406'){alert('동일한 IP를 확인하는 과정에서 DB 조회 시 에러가 났습니다.'); return}
            if(data.status == '407'){alert('접속 테이블에 저장하는 도중 DB 에러가 났습니다.'); return}
            if(data.status == '408'){alert('해당 ID와 PW를 가지는 사용자가 존재하지 않습니다.'); return}
            if(data.status == '409'){alert('입력한 ID와 PW를 가지는 사용자를 조회할 때 DB 에러가 났습니다.'); return}
            if(data.data[0].LOGIN_APPROVAL_FLAG == 'N'){
                alert('로그인 승인이 허가되지않은 사용자 입니다.');
                sessionStorage.clear();
                return;
            }
            if(data.data[0].DELETE_FLAG == 'Y'){
                alert('관리자에 의해 삭제된 사용자 입니다.');
                sessionStorage.clear();
                return;
            }
            if(data.data[0].WITHDRAW_FLAG == 'Y'){
                alert('탈퇴한 사용자 입니다.');
                sessionStorage.clear();
                return;
            }
            sessionStorage.setItem(data.data[0].result_data_3, JSON.stringify(data.data[0]));
            if(data.data[0].result_data_3 === undefined){
                alert("일치하는 정보가 없습니다. 다시 입력해주세요.");
                sessionStorage.clear();
                return
            }


            if (data.data[0].MAIN_AUTH == "MVIEW0002") {
                location.href = '/modulesearch'

            } else {
                location.href = '/keyissue'
            }
        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }
    });
}

//20200508 wonjihoon 로그인 버튼
$(function () {
    $("#loginbtn").click(function () {
        getLogInfo();
    })
});

//20200508 wonjihoon 회원가입 페이지 이동 버튼
$(function () {
    $("#regbtn").click(function () {
        location.href = '/reg';

    })
});


//20200623 wonjihoon config값 저장하는 파일

//20200513 wonjihoon 서버
//20200513 wonjihoon 입력 체크
//20200514 wonjihoon 세션 키
// //20200514 wonjihoon 같은 ip에 로그인이 들어왔을 때 (페이지 시작 시 api 호출)

//20200513 wonjihoon 서버
var apiProtocol = "http";
var apiAdress = "15.164.70.209"; //"192.168.100.106";
var apiPort = "5000";

//20200513 wonjihoon 입력 체크
var check_num = /[0-9]/;	// 숫자
var check_eng = /[a-zA-Z]/;	// 문자
var check_spc = /[~!@#$%^&*()_+|<>?:{}]/; // 특수문자
var check_kor = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/; // 한글체크
var datatimeRegexp = /[0-9]{4}-[0-9]{2}-[0-9]{2}/;//날짜체크
var check_db = /[#\\?/%_]/;// api, db에 안들어가는 문자

//20200514 wonjihoon 세션 키
sessionStorage.removeItem("modulesearch"); //인식모듈 조회 세션 값 삭제
sessionStorage.removeItem("selectbox"); //페이지당 리스트 출력 개수 세션 값 삭제
sessionStorage.removeItem("page"); //선택한 페이지 세션 값 삭제
sessionStorage.removeItem("keysearch"); // 인식키 조회 세션 값 삭제
var SKey = sessionStorage.key(0); // 세션 사용자 키 저장
var SValue = JSON.parse(sessionStorage.getItem(SKey)); // 세션 사용자 키의 밸류 저장

// //20200514 wonjihoon 같은 ip에 로그인이 들어왔을 때 (페이지 시작 시 api 호출)
$(document).ready(function(){

    if(sessionStorage.length == 1) {
        var SKey = sessionStorage.key(0);
        var SValue = JSON.parse(sessionStorage.getItem(SKey));
    }
    if(SKey != null) {
        $.ajax({
            url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/get_access_info/' + SKey,
            type: 'post',
            success: function (data) {
                if(data.status == '400'){alert('사용자 KEY가 존재하지 않습니다.'); return}
                if(data.status == '401'){alert('사용자 IP가 추출되지 않았습니다.'); return}
                if(data.status == '402'){alert('동일한 IP로 접속해 있는 사용자를 조회하는 도중 DB 에러가 났습니다.'); return}

                if (data.status == '201') {
                    alert('같은 ip에서의 다른 로그인으로 인해 로그아웃 되었습니다.');
                    sessionStorage.clear();
                    location.href = '/login';
                }
            },
            error: function (request, status, error) {
                alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                return
            }
        });
    }

});

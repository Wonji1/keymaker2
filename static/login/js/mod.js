//20200623 wonjihoon 자기정보 수정 파일

//20200512 wonjihoon 화면이 켜질때 회사명 리스트 selectbox에 삽입
//20200514 wonjihoon 회원정보 입력
//20200512 wonjihoon 회사등록 버튼
//20200512 wonjihoon 회원수정 기능
//20200512 wonjihoon 수정버튼
//20200512 wonjihoon 수정취소 버튼 시 페이지 이동
//20200512 wonjihoon yes/no 알림창

document.write("<script src='/static/main/js/config.js'></script>");

//20200512 wonjihoon 화면이 켜질때 회사명 리스트 selectbox에 삽입
//20200514 wonjihoon 회원정보 입력
$(document).ready(function(){
    if(SValue != null){// SValue --> config.js 파일에 있으며 session에 저장된 key에 대한 value 값이다 , AUUSE0007은 자기정보 수정 권한이다.
        if(SValue.AUTH.indexOf('AUUSE0007') == -1){history.back(); alert('수정 권한이 존재하지 않습니다. 이전 페이지로 이동합니다.')}}
    $.ajax({
         url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_user_info/'+SKey+'/0/LGUSE0010',
        type: 'get',
        success: function (data) {
            if(data.status == '400'){alert('ID의 값에 영어, 숫자 이외의 문자가 있습니다.'); return}
            if(data.status == '401'){alert('DB 조회할 때 에러가 났습니다.'); return}
            if(data.status == '402'){alert('조회 권한이 존재하지 않습니다.'); return}
            document.getElementById('user_id').value = data.data[0].result_data_1;
            document.getElementById('user_name').value = data.data[0].USER_NAME;
            document.getElementById('user_comp').value = data.data[0].COMPANY_NAME;
            document.getElementById('user_dept').value = data.data[0].DEPARTMENT;
            document.getElementById('user_rank').value = data.data[0].POSITION;
            if(data.data[0].PHONE_NUMBER != null){
            var pnArray = data.data[0].PHONE_NUMBER.split('-');
            document.getElementById('user_pn1').value = pnArray[0];
            document.getElementById('user_pn2').value = pnArray[1];
            document.getElementById('user_pn3').value = pnArray[2];}
            if(data.data[0].EMAIL != null){
            var email1Array = data.data[0].EMAIL.split('@');
            var email2Array = email1Array[1].split('.');
            document.getElementById('user_email1').value = email1Array[0];
            document.getElementById('user_email2').value = email2Array[0];
            document.getElementById('user_email3').value = email2Array[1];}
        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }
    });

    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_company_list/0/0/0/0',
        type: 'get',
        success: function (data) {
            if(data.status == '400'){alert('DB 조회할 때 에러가 났습니다.'); return}
            var str = ''; // 회사 리스트 담을 공간
            for(var i =0; i< data.data.length; i++){
                str += '<option value="' +data.data[i].COMPANY_NAME+ '">'+data.data[i].COMPANY_NAME+'</option>';
            }
            $('#user_comp').html(str);
        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }
    });
})

//20200512 wonjihoon 회사등록 버튼
$(function () {
    $("#add_comp").click(function () {
        window.open('/addcomppop', '', 'top=130, left=10, width=380, height=400, status=no, menubar=no, toolbar=no, resizable=no, titlebar=no, location=no');
    })
});

//20200512 wonjihoon 회원수정 기능
function getmodInfo() {

    var user_pw1 = document.getElementById("user_pw1").value;
    user_pw1 = user_pw1.toLowerCase();
    var user_pw2 = document.getElementById("user_pw2").value;
    user_pw2 = user_pw2.toLowerCase();
    var user_comp = document.getElementById("user_comp").value;
    var user_dept = document.getElementById("user_dept").value;
    var user_rank = document.getElementById("user_rank").value;
    var user_pn1 = document.getElementById("user_pn1").value;
    var user_pn2 = document.getElementById("user_pn2").value;
    var user_pn3 = document.getElementById("user_pn3").value;
    var user_email1 = document.getElementById("user_email1").value;
    var user_email2 = document.getElementById("user_email2").value;
    var user_email3 = document.getElementById("user_email3").value;

    var user_pn = user_pn1 + '-' + user_pn2 +'-' + user_pn3;
    var user_email = user_email1 + '@' + user_email2 +'.' + user_email3;
    if(user_pw1 ==""){
        user_pw1 = 0;
    }
    if (user_comp == "" || user_dept == "" || user_rank == "" || user_pn1 == "" ||
        user_pn2 == "" || user_pn3 == "" || user_email1 == "" || user_email2 == "" || user_email3 == "" ) {
        alert("입력창이 비었습니다.");
        return
    }
    if(check_db.test(user_pw1) || check_db.test(user_pw2) || check_db.test(user_comp) || check_db.test(user_dept) || check_db.test(user_rank) || check_db.test(user_pn1)
        || check_db.test(user_pn2) || check_db.test(user_pn3) ||  check_db.test(user_email1) || check_db.test(user_email2) || check_db.test(user_email3)){
        alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
        return
    }
    if(!check_num.test(user_pw1) && !check_eng.test(user_pw1) || check_spc.test(user_pw1) || user_pw1 != user_pw2 || user_pw1.length >20 ) { alert('비밀번호를 다시 입력해주세요.'); return }
    if(!check_num.test(user_dept) && !check_eng.test(user_dept) && !check_kor.test(user_dept)|| user_dept.length >20) { alert('부서명은 한국어, 영어, 숫자로 작성해주세요.'); return }
    if(!check_num.test(user_pn1) && !check_num.test(user_pn2) && !check_num.test(user_pn3)) { alert('전화번호를 다시 입력해주세요.'); return }

    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/set_user_info/'+SKey+'/LGUSE0010/'+user_pw1+'/0/'+user_comp+'/'+user_dept+'/'+user_rank+'/'+user_pn+'/'+user_email,
        type: 'post',
        success: function (data) {
            if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
            if(data.status == '401'){alert('권한이 존재하지 않습니다.'); return}
            if(data.status == '402'){alert('사용자 정보 수정 도중 DB 에러가 났습니다.'); return}
            alert('수정되었습니다.');
            if (SValue.MAIN_AUTH == "MVIEW0002") { //사용자인지 관리자인지 체크
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

//20200512 wonjihoon 수정버튼
$(function () {
    $("#modbtn").click(function () {
        getmodInfo();
    })
});


//20200512 wonjihoon 수정취소 버튼 시 페이지 이동
$(function () {
    $("#modcancelbtn").click(function () {
        if (SValue.MAIN_AUTH == "MVIEW0002") { //사용자인지 관리자인지 체크
            location.href = '/modulesearch'

        } else {
            location.href = '/keyissue'
        }
    })
});

//20200512 wonjihoon yes/no 알림창
$(function () {
    $("#talbtn").click(function () {
        var result = confirm('정말 탈퇴하시겠습니까?');
        if(result) { $.ajax({
            url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/set_user_wih_del_flag/'+SKey+'/LGUSE0011',
            type: 'post',
            success: function (data) {
                if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
                if(data.status == '401'){alert('권한이 존재하지 않습니다.'); return}
                if(data.status == '402'){alert('탈퇴 혹은 사용자 삭제 도중 DB 에러가 났습니다.'); return}
                alert('탈퇴되었습니다.');
                location.href = '/login'
            },
            error:function(request,status,error){
                alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                return
            }
        });}
        else { return }

    })
});

//20200623 wonjihoon 회원가입 파일

//20200511 wonjihoon 회원가입 기능
//20200511 wonjihoon 회원가입 취소 버튼
//20200511 wonjihoon 회원가입 버튼
//20200511 wonjihoon 회사등록 버튼
//20200512 wonjihoon id 중복확인 버튼
//20200519 wonjihoon id 중복확인 후 입력창 입력 방지
//20200512 wonjihoon 화면이 켜질때 회사명 리스트 selectbox에 삽입
// 20200519 wonjihoon 방지된 입력창 해제하는 버튼

document.write("<script src='/static/main/js/config.js'></script>");

//20200511 wonjihoon 회원가입 기능
function getregInfo() {

    var user_id = document.getElementById("user_id").value;
    user_id = user_id.toLowerCase();
    var user_pw1 = document.getElementById("user_pw1").value;
    user_pw1 = user_pw1.toLowerCase();
    var user_pw2 = document.getElementById("user_pw2").value;
    user_pw2 = user_pw2.toLowerCase();
    var user_name = document.getElementById("user_name").value;
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

    if (user_id == "" || user_pw1 == "" || user_pw2 == "" || user_name == "" || user_comp == "" || user_dept == "" || user_rank == "" || user_pn1 == "" ||
        user_pn2 == "" || user_pn3 == "" || user_email1 == "" || user_email2 == "" || user_email3 == "" ) {
        alert("입력창이 비었습니다.");
        return
    }
    if(check_db.test(user_id) || check_db.test(user_pw1) || check_db.test(user_pw2) ||check_db.test(user_comp) || check_db.test(user_dept) || check_db.test(user_rank)
        || check_db.test(user_pn1) || check_db.test(user_pn2) || check_db.test(user_pn3) || check_db.test(user_email1) || check_db.test(user_email2) || check_db.test(user_email3)){
        alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
        return
    }

    if(!check_num.test(user_id) && !check_eng.test(user_id) || check_spc.test(user_id) || user_id.length >20) { alert('아이디는 특수문자 x, 대소문자 구분x, 영문 숫자를 20자 이내로 작성해주세요.'); return }
    if(!check_num.test(user_pw1) && !check_eng.test(user_pw1) || check_spc.test(user_pw1) || user_pw1 != user_pw2 || user_pw1.length >20) { alert('비밀번호를 다시 입력해주세요.'); return }
    if(check_spc.test(user_name) || user_name.length >25) { alert('이름은 특수문자 x, 25자 이내로 작성.'); return }
    if(!check_num.test(user_dept) && !check_eng.test(user_dept) && !check_kor.test(user_dept)|| user_dept.length >20) { alert('부서명은 한국어, 영어, 숫자를 20자 이내로 작성해주세요.'); return }
    if(!check_num.test(user_pn1) && !check_num.test(user_pn2) && !check_num.test(user_pn3)) { alert('전화번호를 다시 입력해주세요.'); return }


    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/add_user_info/'+user_id+'/'+user_pw1+'/'+user_name+'/'+user_comp+'/'+user_dept+'/'+user_rank+'/'
            +user_pn+'/'+user_email,
        type: 'post',
        success: function (data) {
            if(data.status == '421'){alert('동일한 ID 조회 과정에서 DB 에러가 났습니다.'); return}
            if(data.status == '422'){alert('동일한 ID가 존재합니다.'); return}
            if(data.status == '423'){alert('동일한 회사명 조회 과정에서 DB 에러가 났습니다.'); return}
            if(data.status == '424'){alert('동일한 회사명이 존재하지 않습니다.'); return}
            if(data.status == '425'){alert('사용자 정보 저장 도중 DB 에러가 났습니다.'); return}
            alert('등록되었습니다.');
            location.href ='/login';
        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }
    });

}
//20200511 wonjihoon 회원가입 취소 버튼
$(function () {
    $("#reg_cancel").click(function () {
        location.href = '/login';

    })
});

//20200511 wonjihoon 회원가입 버튼
$(function () {
    $("#reg").click(function () {
        if(document.getElementById('id_label').value =='201'){ // 중복확인 여부 판단
            getregInfo();
            return
        }
        if(document.getElementById('id_label').value =='200' || document.getElementById('id_label').value == null){
            alert('아이디 중복확인을 해주세요.');
            return
        }
        else{
            alert('입력값들을 다시 확인해주세요.');
            return
        }
    })
});

//20200511 wonjihoon 회사등록 버튼
$(function () {
    $("#add_comp").click(function () {
        window.open('/addcomppop', '', 'top=130, left=10, width=500, height=420, status=no, menubar=no, toolbar=no, resizable=no, titlebar=no, location=no');
    })
});

//20200512 wonjihoon id 중복확인 버튼
//20200519 wonjihoon id 중복확인 후 입력창 입력 방지
$(function () {
    $("#id_checkbtn").click(function () {
        var user_id = document.getElementById("user_id").value;
        if(user_id == ''){

            alert('아이디 값을 넣어주세요.');
            return
        }
        if(!check_num.test(user_id) && !check_eng.test(user_id) || check_spc.test(user_id) || user_id.length >20) { alert('아이디는 특수문자 x, 대소문자 구분x, 영문 숫자를 20자 이내로 작성해주세요.'); return }



        $.ajax({
            url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_user_info/0/' +user_id + '/0' ,
            type: 'get',

            success: function (data) {
                if(data.status == '400'){alert('ID의 값에 영어, 숫자 이외의 문자가 있습니다.'); return}
                if(data.status == '401'){alert('DB 조회할 때 에러가 났습니다.'); return}
                if(data.status == '402'){alert('조회 권한이 존재하지 않습니다.'); return}
                if(data.status == '200'){
                    alert('존재하는 id 입니다. 다시 입력해 주세요.');
                }
                if(data.status == '201'){
                    var result = confirm('사용가능한 id 입니다. 사용하시겠습니까?');
                    if(result) {
                        $("#id_checkbtn").hide();
                        $("#id_modbtn").show();
                        document.getElementById('user_id').style.borderWidth = "0px";
                        document.getElementById('user_id').readOnly = true;             //중복 확인 후 입력 방지

                    }
                    else { return }
                }
                document.getElementById('id_label').value = data.status;
            },
            error:function(request,status,error){
                alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                return
            }
        });
    })
});


//20200512 wonjihoon 화면이 켜질때 회사명 리스트 selectbox에 삽입
$(document).ready(function(){
    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_company_list/0/0/0/0',
        type: 'get',
        success: function (data) {
            if(data.status == '400'){alert('DB 조회할 때 에러가 났습니다.'); return}
            var str = ''; //회사 리스트 담을 공간
            for(var i =0; i< data.data.length; i++){
                str += '<option style="font-size: 1em" value="' +data.data[i].COMPANY_NAME+ '">'+data.data[i].COMPANY_NAME+'</option>';
            }
            $('#user_comp').html(str);
        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }
    });
})

// 20200519 wonjihoon 방지된 입력창 해제하는 버튼
$(function () {
    $("#id_modbtn").click(function () {

        document.getElementById('id_label').value = null;
        $("#id_modbtn").hide();
        $("#id_checkbtn").show();
        document.getElementById('user_id').style.borderWidth = "1px";
        document.getElementById('user_id').readOnly = false;            //다시입력 버튼 클릭 시 아이디 입력할 수 있게하고 중복확인 value null로 전환

    })
});
//20200623 wonjihoon 로그인 이후 공통으로 들어가는 코드 파일

//20200508 wonjihoon main UI
//20200514 wonjihoon 세션이 없는사람이 페이지를 들어왔을 시 로그인페이지로 이동
//20200521 wonjihoon 권한메뉴
//20200511 wonjihoon 로그아웃
//20200512 wonjihoon 상단 이미지 클릭시 메인페이지 이동
//20200513 wonjihoon 회원정보수정 버튼

document.write("<script src='/static/main/js/config.js'></script>");

//20200508 wonjihoon main UI
//20200514 wonjihoon 세션이 없는사람이 페이지를 들어왔을 시 로그인페이지로 이동
//20200521 wonjihoon 권한메뉴
$(document).ready(function () {
    $('#sessionval').show();

    if (SValue == null) {
        alert('로그인을 진행해 주세요.');
        location.href = '/login'
    } else {
        if (SValue.MAIN_AUTH == "MVIEW0002") {
            document.getElementById("sessionuser").innerHTML = "관리자";
            document.getElementById("sessionname").innerHTML = SValue.USER_NAME;
            document.getElementById("navbar").style.backgroundColor = "#616A6B";
            document.getElementById("footer").style.backgroundColor = "#616A6B";

        } else {
            document.getElementById("sessionuser").innerHTML = "사용자";
            document.getElementById("sessionname").innerHTML = SValue.USER_NAME;

        }

    }

    if(SValue.AUTH.indexOf('AUCHA0001') != -1 || SValue.AUTH.indexOf('AUCHA0002') != -1 || SValue.AUTH.indexOf('AUCHA0003') != -1 || SValue.AUTH.indexOf('AUCHA0004') != -1){$("#sub_auth").show();}
    if(SValue.AUTH.indexOf('AUKEY0001') != -1 || SValue.AUTH.indexOf('AUKEY0002') != -1 || SValue.AUTH.indexOf('AUKEY0003') != -1 || SValue.AUTH.indexOf('AUKEY0004') != -1 || SValue.AUTH.indexOf('AUKEY0005') != -1){$("#menu_key").show();}
    if(SValue.AUTH.indexOf('AUKEY0001') != -1 || SValue.AUTH.indexOf('AUKEY0002') != -1){$("#sub_keyissue").show();}
    if(SValue.AUTH.indexOf('AUKEY0003') != -1){$("#sub_keysearch").show();}
    //if(SValue.AUTH.indexOf('AUKEY0004') != -1){$("#sub_keygis").show();}
    //if(SValue.AUTH.indexOf('AUKEY0005') != -1){$("#sub_keystatic").show();}
    if(SValue.AUTH.indexOf('AUMOD0001') != -1 || SValue.AUTH.indexOf('AUMOD0005') != -1){$("#menu_module").show();}
    if(SValue.AUTH.indexOf('AUMOD0001') != -1){$("#sub_modulesearch").show();}
    if(SValue.AUTH.indexOf('AUMOD0005') != -1){$("#sub_moduleadd").show();}
    //if(SValue.AUTH.indexOf('AUNOT0001') != -1 || SValue.AUTH.indexOf('AUNOT0004') != -1){$("#menu_notice").show();}
    //if(SValue.AUTH.indexOf('AUNOT0001') != -1){$("#sub_notsearch").show();}
    //if(SValue.AUTH.indexOf('AUNOT0004') != -1){$("#sub_notadd").show();}
    //if(SValue.AUTH.indexOf('AUSYS0001') != -1 || SValue.AUTH.indexOf('AUSYS0002') != -1 || SValue.AUTH.indexOf('AUSYS0003') != -1){$("#menu_adsys").show();}
    //if(SValue.AUTH.indexOf('AUSYS0001') != -1){$("#sub_logsearch").show();}
    //if(SValue.AUTH.indexOf('AUSYS0002') != -1){$("#sub_moddate").show();}
    //if(SValue.AUTH.indexOf('AUSYS0003') != -1){$("#sub_backdb").show();}
    //if(SValue.AUTH.indexOf('AUUSE0001') != -1 || SValue.AUTH.indexOf('AUUSE0004') != -1 || SValue.AUTH.indexOf('AUUSE0005') != -1){$("#menu_aduser").show();}
    //if(SValue.AUTH.indexOf('AUUSE0001') != -1){$("#sub_usersearch").show();}
    //if(SValue.AUTH.indexOf('AUUSE0004') != -1){$("#sub_useradd").show();}
    //if(SValue.AUTH.indexOf('AUUSE0005') != -1){$("#sub_approval").show();}




});

//20200511 wonjihoon 로그아웃
$(function () {
    $("#logout").click(function () {
        $.ajax({
            url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/ip',
            type: 'get',
            success: function (data) {
                $.ajax({
                    url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/logout/' + data,
                    type: 'post',
                    success: function(data){
                        if(data.status == '400'){alert('IP 추출이 제대로 적용되지 않았습니다.'); return}
                        if(data.status == '401'){alert('동일한 IP로 접속한 사용자가 없습니다.'); return}
                        if(data.status == '402'){alert('동일한 IP로 접속한 사용자 조회 시 DB 에러가 났습니다.'); return}
                    },
                    error: function (request, status, error) {
                        alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                        return
                    }
                });
            },
            error: function (request, status, error) {
                alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                return
            }
        });
        sessionStorage.clear();
        location.href = '/login';
    })
});

//20200512 wonjihoon 상단 이미지 클릭시 메인페이지 이동
$(function () {
    $("#toplogo").click(function () {
        var SKey = sessionStorage.key(0); // SValue --> config.js 파일에 있으며 session에 저장된 key
        var SValue = JSON.parse(sessionStorage.getItem(SKey));// SValue --> config.js 파일에 있으며 session에 저장된 key에 대한 value 값

        if (SValue.MAIN_AUTH == "MVIEW0002") { // 사용자인지 관리자인지 판단
            location.href = '/modulesearch'

        } else {
            location.href = '/keyissue'
        }
    })
});

//20200513 wonjihoon 회원정보수정 버튼
$(function () {
    $("#sessionname").click(function () {
        location.href = '/mod'

    })
});

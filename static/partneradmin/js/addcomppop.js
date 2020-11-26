//20200623 wonjihoon 업체등록 팝업창 파일

//20200513 wonjihoon 회사등록, 부모창 업체명 새로고침
//20200512 wonjihoon 업체등록
//20200512 wonjihoon 업체명 중복확인
// 20200519 wonjihoon 방지된 입력창 해제하는 버튼

document.write("<script src='/static/main/js/config.js'></script>");

//20200513 wonjihoon 회사등록, 부모창 업체명 새로고침
function getcompInfo() {

    var comp_name = document.getElementById("comp_name").value;
    var comp_addr = document.getElementById("comp_addr").value;
    var comp_memo = document.getElementById("comp_memo").value;
    var comp_pn1 = document.getElementById("comp_pn1").value;
    var comp_pn2 = document.getElementById("comp_pn2").value;
    var comp_pn3 = document.getElementById("comp_pn3").value;
    var comp_email1 = document.getElementById("comp_email1").value;
    var comp_email2 = document.getElementById("comp_email2").value;
    var comp_email3 = document.getElementById("comp_email3").value;

    var comp_pn = comp_pn1 + '-' + comp_pn2 +'-' + comp_pn3;
    var comp_email = comp_email1 + '@' + comp_email2 +'.' + comp_email3;

    if (comp_name == "" ||  comp_addr == "" || comp_memo == "" || comp_pn1 == "" ||
        comp_pn2 == "" || comp_pn3 == "" || comp_email1 == "" || comp_email2 == "" || comp_email3 == "" ) {
        alert("입력창이 비었습니다.");
        return
    }
    if(check_db.test(comp_name) || check_db.test(comp_addr) || check_db.test(comp_memo) || check_db.test(comp_pn1)
        || check_db.test(comp_pn2) || check_db.test(comp_pn3) ||check_db.test(comp_email3) ||check_db.test(comp_email2) || check_db.test(comp_email1)){
        alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
        return false
    }

    if(comp_name.length >20) { alert('업체명은 20자 이내로 작성해주세요.'); return }
    if(comp_addr.length >100) { alert('주소는 100자 이내로 작성해주세요.'); return }
    if(comp_memo.length >100) { alert('메모는 100자 이내로 작성해주세요.'); return }
    if(!check_num.test(comp_pn1) && !check_num.test(comp_pn2) && !check_num.test(comp_pn3)) { alert('전화번호는 숫자로 입력해주세요.'); return }
    if(!check_num.test(comp_email1) && !check_eng.test(comp_email1) && !check_num.test(comp_email2) && !check_eng.test(comp_email2) && !check_num.test(comp_email3)&& !check_eng.test(comp_email3) ) { alert('이메일을 다시 입력해주세요.'); return }


    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/add_company_list/0/'+comp_name+'/'+comp_addr+'/'+comp_pn+'/'+comp_email+'/'+comp_memo+'/0/0/0',
        type: 'post',
        success: function (data) {
            if(data.status == '400'){alert('업체명이 중복되었습니다.'); return}
            if(data.status == '402'){alert('업체명 타입이 부적합 합니다.'); return}
            if(data.status == '404'){alert('주소 타입이 부적합 합니다.'); return}
            if(data.status == '406'){alert('전화번호 타입이 부적합 합니다.'); return}
            if(data.status == '408'){alert('이메일 타입이 부적합 합니다.'); return}
            if(data.status == '410'){alert('메모 타입이 부적합 합니다.'); return}
            if(data.status == '414'){alert('업체를 저장하는 도중 DB 조회할 때 에러가 났습니다.'); return}
            if(data.status == '415'){alert('업체를 저장하고 저장한 업체 리스트를 불러오는 곳에서 DB 조회할 때 에러가 났습니다.'); return}

            alert('등록되었습니다.');
            var str =''; // 부모 페이지의 회사 리스트 갱신을 담는 공간
                    for(var i =0; i< data.data.length; i++){
                        str += '<option value="' +data.data[i].COMPANY_NAME+ '">'+data.data[i].COMPANY_NAME+'</option>';
                    }
                    window.opener.document.getElementById("user_comp").innerHTML = str;

                    window.close();
        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }
    });

}

//20200512 wonjihoon 업체등록
$(function () {
    $("#pop_addbtn").click(function () {
        if(document.getElementById('comp_label').value !='201'){
            alert('업체명 중복확인을 해주세요.');
            return
        }
        getcompInfo();
})});

//20200512 wonjihoon 업체명 중복확인
$(function () {
    $("#comp_checkbtn").click(function () {
        var comp_name = document.getElementById("comp_name").value;
        if(comp_name == ''){

            alert('업체명 값을 넣어주세요.');
            return
        }
        $.ajax({
            url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_company_list/0/'+ comp_name+'/0/0',
            type: 'get',
            success: function (data) {
                if(data.status == '200'){
                    alert('존재하는 업체명 입니다. 다시 입력해 주세요.');
                }
                if(data.status == '201'){
                    var result = confirm('사용가능한 업체명입니다. 사용하시겠습니까?');
                    if(result) {
                        $("#comp_checkbtn").hide();
                        $("#comp_modbtn").show();
                        document.getElementById('comp_name').style.borderWidth = "0px";
                        document.getElementById('comp_name').readOnly = true;

                    }
                    else { return }
                }
                if(data.status == '400'){
                    alert('조회가 이루어지지 않았습니다.');
                }
                document.getElementById('comp_label').value = data.status;
            },
            error:function(request,status,error){
                alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                return
            }
        });
    })
});

// 20200519 wonjihoon 방지된 입력창 해제하는 버튼
$(function () {
    $("#comp_modbtn").click(function () {

        document.getElementById('comp_label').value = null;
        $("#comp_modbtn").hide();
        $("#comp_checkbtn").show();
        document.getElementById('comp_name').style.borderWidth = "1px";
        document.getElementById('comp_name').readOnly = false;

    })
});

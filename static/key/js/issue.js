//20200623 wonjihoon 인식키 발급하는 파일

//20200602 wonjihoon 권한이 없으면 이전 페이지로 이동
//20200526 wonjihoon 핸드폰 확인하는 함수
//20200603 wonjihoon ip.pe API 사용해서 IP 추출
//20200526 wonjihoon input type='file' 을 CAMERA 버튼으로 대체
//20200526 wonjihoon input type='file' 을 업로드 버튼으로 대체
//20200527 wonjihoon 카메라에서 찍은 파입 업로드 시 이름 표출
//20200527 wonjihoon 발급취소 버튼
//20200527 wonjihoon 키 발급 버튼
//20200528 wonjihoon 키 발급 완료 버튼
//20200528 wonjihoon 키 발급 api 사용

document.write("<script src='/static/main/js/config.js'></script>");

//20200602 wonjihoon 권한이 없으면 이전 페이지로 이동
$(document).ready(function () {
    if(SValue !=null){
    if(SValue.AUTH.indexOf('AUKEY0001') == -1 && SValue.AUTH.indexOf('AUKEY0002') == -1){history.back();alert('인식키 발급 권한이 존재하지 않습니다. 이전 페이지로 이동합니다.')}}
}); // SValue --> config.js 파일에 있으며 session에 저장된 key에 대한 value 값이다 , AUKEY0001, AUKEY0002 는 직원, 파트너 인식키 발급 권한이다.

//20200526 wonjihoon 핸드폰 확인하는 함수
function isMobile() {
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

//20200603 wonjihoon ip.pe API 사용해서 IP 추출
function getLocation() {

    $.ajax({
        url: 'https://api.ip.pe.kr/json/',
        type: 'get',
        async: false,
        success: function (data) {
            document.getElementById('ip').value = data.ip;
        },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            return
        }
    })}

//20200526 wonjihoon input type='file' 을 버튼으로 대체
$(function () {
    $("#cambtn").click(function (e) {
        if(isMobile()) {
            e.preventDefault();
            $('#cam').click();
        }
        else{alert('PC에서는 사용할 수 없는 기능입니다.');}

    })
});

//20200526 wonjihoon input type='file' 을 버튼으로 대체
$(function () {
    $("#uploadbtn").click(function (e) {
        e.preventDefault();
            $('#cam').click();
    })
});

//20200527 wonjihoon 카메라에서 찍은 파입 업로드 시 이름 표출
$(function () {
    $('#cam').change(function (e) {
        if(document.getElementById('cam').files[0] != '') {
            $('#img_div').empty();
            var strFile = '';
            strFile += document.getElementById('cam').files[0].name;
            $("#file_span").html(strFile);//파일명 추가하는 코드

            var reader = new FileReader();
            reader.onload = function (event) {
                var img = document.createElement("img");
                img.setAttribute("src", event.target.result);
                img.setAttribute('width', '100px');
                img.setAttribute('height', '100px');
                document.querySelector("div#img_div").appendChild(img); //이미지 추가하는 코드
            };
            reader.readAsDataURL(event.target.files[0]);

            var sendingData = new FormData();
            sendingData.append('read_qr_user_key',SKey);
            sendingData.append('read_qr_image',document.getElementById('cam').files[0]);
            sendingData.append('read_qr_image_name', document.getElementById('cam').files[0].name);
            sendingData.append('read_qr_image_size',document.getElementById('cam').files[0].size); //FORM에 데이터 추가하는 코드

            $.ajax({
                url:  apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/read_qr',
                processData: false,
                contentType: false,
                data: sendingData,
                type: 'POST',
                success: function (data) {
                    console.log(data);
                    if (data.status == '400') {alert('접속해 있는 사용자가 아닙니다.');return}
                    if (data.status == '401') {alert('접속 여부 확인 도중 DB 에러가 났습니다.');return}
                    if (data.status == '402') {alert('이미지가 제대로 입력되지 않았습니다.');return}
                    if (data.status == '403') {alert('이미지가 제대로 인식되지 않았습니다. 계속해서 실패할 경우 QR코드 값을 입력해주세요.');return}
                    document.getElementById('qr1').value = data.data[0].qr_key.substr(0,4);
                    document.getElementById('qr2').value = data.data[0].qr_key.substr(4,4);
                    document.getElementById('qr3').value = data.data[0].qr_key.substr(8,4);
                    document.getElementById('qr4').value = data.data[0].qr_key.substr(12,4);
                    document.getElementById('read_qr_index').value = data.data[0].index;
                },
                error: function (request, status, error) {
                    alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                    return
                }
            })
        }

    })
});

//20200527 wonjihoon 발급취소 버튼
$(function () {
    $("#cancel_key").click(function () {
        var result = confirm('수정을 취소하시겠습니까?');
        if(result) {location.href='/keysearch'}
        else { return }
    })
});

//20200527 wonjihoon 키 발급 버튼
$(function () {
    $("#issue_key").click(function () {
        getLocation();
        issueKeyApi();
    })
});

//20200528 wonjihoon 키 발급 완료 버튼
$(function () {
    $("#complete_key").click(function () {
        var result = confirm('완료 시 발급된 키는 사라집니다. 키 발급을 완료하시겠습니까?');
        if(result) {if (SValue.MAIN_AUTH == "MVIEW0002") {
            location.href = '/keysearch'

        } else {
            location.href = '/keyissue'
        }}
        else { return }
    })
});

//20200528 wonjihoon 키 발급 api 사용
function  issueKeyApi() {
    var boxtf = 'new';
    if (document.getElementById('qr1').value.length != 4 ||document.getElementById('qr2').value.length != 4
        || document.getElementById('qr3').value.length != 4 || document.getElementById('qr4').value.length != 4) {
        alert("QR코드 입력창 마다 4글자씩 입력해 주세요.");
        document.getElementById('qr1').focus();
        return}
    var qr = document.getElementById('qr1').value + document.getElementById('qr2').value + document.getElementById('qr3').value + document.getElementById('qr4').value;
    if(document.getElementById('boxbtn').checked == true){
        boxtf = 'old';
    }
    var memo;
    if(document.getElementById('qr_memo').value.length > 100){
        alert("메모를 100자 이내로 입력해주세요.");
        document.getElementById('qr_memo').focus();
        return
    }
    memo  =document.getElementById('qr_memo').value;
    if(document.getElementById('qr_memo').value ==''){
        memo = 0;
    }
    $.ajax({
        url:  apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/issue_key/'+ SKey +'/'+document.getElementById('read_qr_index').value+'/'+document.getElementById('ip').value+'/' + qr + '/' + boxtf + '/'+ memo,
        type: 'POST',
        success: function (data) {
            console.log(data);
            if (data.status == '400') {alert('접속해 있는 사용자가 아닙니다.');return}
            if (data.status == '401') {alert('접속 여부 확인 도중 DB 에러가 났습니다.');return}
            if (data.status == '403') {alert('check_version API가 호출되지 않았습니다.');return}
            if (data.status == '404') {alert('create_key API가 호출되지 않았습니다.');return}
            if (data.status == '405') {alert('인식키 발급 권한이 존재하지 않습니다.');return}
            $('#key_val').html(data.data[0].Key);
            $('#cancel_key').hide();
            $('#issue_key').hide();
            $('#complete_key').show();
        },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            return
        }
    })
}
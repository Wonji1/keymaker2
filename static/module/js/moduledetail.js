//20200623 wonjihoon 모듈 조회 상세 파일

//20200520 wonjihoon 모듈 상세 정보 표출
//20200602 wonjihoon 모듈 조회 권한이 존재하지 않을 시 이전 페이지로 이동
//20200521 wonjihoon 수정버튼
//20200521 wonjihoon 삭제버튼
//20200521 wonjihoon 목록버튼

document.write("<script src='/static/main/js/config.js'></script>");

//20200520 wonjihoon 모듈 상세 정보 표출
//20200602 wonjihoon 모듈 조회 권한이 존재하지 않을 시 이전 페이지로 이동
$(document).ready(function(){
    if(SValue != null){//SValue --> config.js 파일에 있으며 session에 저장된 key에 대한 value 값이다 , AUKMOD0001은 인식모듈 조회 권한이다.
        if(SValue.AUTH.indexOf('AUMOD0001') == -1){history.back(); alert('모듈 조회 권한이 존재하지 않습니다. 이전 페이지로 이동합니다.')}}
    $.ajax({
        url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/get_module_info/' + SKey +'/LGMOD0001/'+ document.getElementById("idx").value,
        type: 'post',
        success: function (data) {
            if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
            if(data.status == '402'){alert('인식모듈을 작성한 사용자가 아닙니다.'); return}
            if(data.status == '403'){alert('인식모듈 정보를 불러오는 도중 DB 에러가 났습니다.'); return}
            if(data.status == '404'){alert('입력값에서 디비 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.'); return}
            if(data.status == '405'){alert('삭제되었거나 존재하지 않는 인식모듈 입니다.'); return}
            if(SValue.AUTH.indexOf('AUMOD0003') != -1 || data.data[0].id_equal_flag == 'Y'){
                $("#mod_module").show();
            }
            if(SValue.AUTH.indexOf('AUMOD0004') != -1 || data.data[0].id_equal_flag == 'Y'){
                $("#del_module").show();
            }// 수정, 삭제 권한 확인 (본인 OR 권한 존재 시 버튼 표시)

            $("#existflag").val(data.data[0].FILE_EXIST_FLAG);
            $("#module_name").html(data.data[0].MODULE_NAME);
            $("#module_version").html(data.data[0].VERSION);
            $("#module_author").html(data.data[0].USER_NAME);
            $("#module_click").html(data.data[0].COUNT_CLICK);
            $("#module_time").html(data.data[0].DATE_REG +'&nbsp;&nbsp;&nbsp'+ data.data[0].TIME_REG);
            var filesize = (data.data[0].FILE_SIZE/1024).toFixed(3) +'KB';
            if(data.data[0].FILE_SIZE >= 1024 * 1024){
                filesize = (data.data[0].FILE_SIZE/1024/1024).toFixed(3) + 'MB';
            }
            var strFile = ''; // 다운로드 담을 공간
            if(data.data[0].FILE_EXIST_FLAG == 'N'){
                strFile = '';
            }
            else {
                strFile += '<a style="font-size: 1em;" href="'+apiProtocol+ '://' + apiAdress + ':'+ apiPort + '/api/down_module/' + SKey + '/' +  document.getElementById("idx").value+'">' + data.data[0].FILE_NAME_ORI + '</a> <span style="font-size: 1em;">&nbsp; [용량: ' + filesize + ']</span> ' +
                '<span style="color: silver;font-size: 1em;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;다운로드 : '+data.data[0].COUNT_DOWN+'</span>';
            }
            $("#module_file").html(strFile);
            $("#module_memo").html(data.data[0].MEMO);

        },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            return
        }
    });

});

//20200521 wonjihoon 수정버튼
$(function () {
    $("#mod_module").click(function () {
        location.href = '/modulemod/'+ document.getElementById('idx').value;

    })
});

//20200521 wonjihoon 삭제버튼
$(function () {
    $("#del_module").click(function () {
        var result = confirm('정말 삭제하시겠습니까?');
        if(result) { $.ajax({
            url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/del_module_info/'+SKey+'/'+document.getElementById('idx').value+'/'+document.getElementById('existflag').value,
            type: 'post',
            success: function (data) {
                if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
                if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
                if(data.status == '402'){alert('작성자가 아니고 인식모듈 삭제 권한이 존재하지 않습니다.'); return}
                if(data.status == '404'){alert('인식모듈 삭제 도중 DB 에러가 났습니다.'); return}
                alert('삭제되었습니다.');
                location.href = '/modulesearch'
            },
            error:function(request,status,error){
                alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                return
            }
        });}
        else { return }

    })
});

//20200521 wonjihoon 목록버튼
$(function () {
    $("#mn_module").click(function () {
        location.href = '/modulesearch'

    })
});

//20200623 wonjihoon 모듈 등록 파일

//20200519 wonjihoon 모듈 등록 유효성 검사
//20200521 wonjihoon 파일없이 모듈등록
//20200518 wonjihoon 업로드 진행률
//20200519 wonjihoon 등록 취소 버튼
//20200522 wonjihoon 키값과 이름 저장
//20200602 wonjihoon 모듈 등록 권한 존재하지 않을 시 이전페이지
//20200522 wonjihoon 첨부파일 첨부 시 정보 표출
//20200529 wonjihoon input type='file' 을 버튼으로 대체
//20200529 wonjihoon X 버튼

document.write("<script src='/static/main/js/config.js'></script>");

//20200519 wonjihoon 모듈 등록 유효성 검사
function formChk(){
    if(document.getElementById('upload_file_file').value !='') {
        document.getElementById('upload_file_file_name').value = document.getElementById('upload_file_file').files[0].name;
        document.getElementById('upload_file_file_size').value = document.getElementById('upload_file_file').files[0].size;
        if(check_db.test(document.getElementById('add_module_info_module_name')) || check_db.test(document.getElementById('add_module_info_version'))
            || check_db.test(document.getElementById('add_module_info_memo'))){
            alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
            return false
        }
        if (document.getElementById('add_module_info_module_name').value == '' || document.getElementById('add_module_info_module_name').value.length > 30) {
            alert("모듈명을 30자 이내로 입력하세요!!");
            document.getElementById('add_module_info_module_name').focus();
            return false
        } else if (document.getElementById('add_module_info_version').value == '' || document.getElementById('add_module_info_version').value.length > 30) {
            alert("버전을 입력하세요!!");
            document.getElementById('add_module_info_version').focus();
            return false
        } else if (document.getElementById('upload_file_file_size').value > 500 * 1024 * 1024) {
            alert("파일을 500MB 이내로 첨부하세요!!");
            return false
        } else if (document.getElementById('add_module_info_memo').value == '' || document.getElementById('add_module_info_memo').value.length > 300) {
            alert("메모를 300자 이내로 입력하세요!!");
            document.getElementById('add_module_info_memo').focus();
            return false
        } else {
            $.ajax({
                url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/add_module_info/' + SKey + '/' + document.getElementById('add_module_info_module_name').value + '/'
                    + document.getElementById('add_module_info_version').value + '/' + document.getElementById('add_module_info_memo').value,
                type: 'post',
                async: false,
                success: function (data) {
                    if (data.status == '400') {
                        alert('접속해 있는 사용자가 아닙니다.');
                        return
                    }
                    if (data.status == '401') {
                        alert('접속 여부 확인 도중 DB 에러가 났습니다.');
                        return
                    }
                    if (data.status == '402') {
                        alert('인식모듈 등록 권한이 존재하지 않습니다.');
                        return
                    }
                    if (data.status == '403') {
                        alert('인식모듈 정보를 불러오는 도중 DB 에러가 났습니다.');
                        return
                    }
                    if (data.status == '404') {
                        alert('입력값에서 DB 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.');
                        return
                    }

                    document.getElementById('upload_file_index').value = data.data[0].index;
                },
                error: function (request, status, error) {
                    alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                    return
                }
            });
        }

            return true

    }
    return false
}

//20200521 wonjihoon 파일없이 모듈등록
$(function () {
    $("#add_module2").click(function () {
        if(document.getElementById('upload_file_file').value =='') {
            if(check_db.test(document.getElementById('add_module_info_module_name')) || check_db.test(document.getElementById('add_module_info_version'))
                || check_db.test(document.getElementById('add_module_info_memo'))){
                alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
                return
            }
            if (document.getElementById('add_module_info_module_name').value == '' || document.getElementById('add_module_info_module_name').value.length > 30) {
                alert("모듈명을 30자 이내로 입력하세요!!");
                document.getElementById('add_module_info_module_name').focus();
                return
            } else if (document.getElementById('add_module_info_version').value == '' || document.getElementById('add_module_info_version').value.length > 30) {
                alert("버전을 입력하세요!!");
                document.getElementById('add_module_info_version').focus();
                return
            } else if (document.getElementById('add_module_info_memo').value == '' || document.getElementById('add_module_info_memo').value.length > 300) {
                alert("메모를 300자 이내로 입력하세요!!");
                document.getElementById('add_module_info_memo').focus();
                return
            }

            $.ajax({
                url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/add_module_info/' + SKey + '/' + document.getElementById('add_module_info_module_name').value + '/'
                    + document.getElementById('add_module_info_version').value + '/' + document.getElementById('add_module_info_memo').value,
                type: 'post',
                success: function (data) {
                    if (data.status == '400') {
                        alert('접속해 있는 사용자가 아닙니다.');
                        return
                    }
                    if (data.status == '401') {
                        alert('접속 여부 확인 도중 DB 에러가 났습니다.');
                        return
                    }
                    if (data.status == '402') {
                        alert('인식모듈 등록 권한이 존재하지 않습니다.');
                        return
                    }
                    if (data.status == '403') {
                        alert('인식모듈 정보를 불러오는 도중 DB 에러가 났습니다.');
                        return
                    }
                    if (data.status == '404') {
                        alert('입력값에서 DB 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.');
                        return
                    }

                    alert('등록되었습니다.');
                    location.href = '/moduledetail/' + data.data[0].index;
                },
                error: function (request, status, error) {
                    alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                    return
                }
            });
        }
    })
});

//20200518 wonjihoon 업로드 진행률
$(function() {
        var bar = $('.bar');
        var percent = $('.percent');
        var status = $('#status');
        $('form').ajaxForm({
            beforeSend: function () {
                status.empty();
                var percentVal = '0%';
                bar.width(percentVal);
                percent.html(percentVal);
            },
            uploadProgress: function (event, position, total, percentComplete) {
                var percentVal = percentComplete + '%';
                bar.width(percentVal);
                percent.html(percentVal);
            },
            success: function (xhr) {
                if (xhr.status == '400') {
                    alert('파일이 제대로 입력되지 않았습니다.');
                    return
                }
                if (xhr.status == '401') {
                    alert('테이블에 저장하는 도중 DB 에러가 발생했습니다.');
                    return
                }

                alert('모듈이 등록되었습니다.');
                location.href = '/moduledetail/' + document.getElementById('upload_file_index').value;
            },
            error: function (e) {
                alert('모듈 등록에 실패하였습니다.');
                return
            }

        });

});

//20200519 wonjihoon 등록 취소 버튼
$(function () {
    $("#cancel_module").click(function () {
        var result = confirm('등록을 취소하시겠습니까?');
        if(result) {location.href = '/modulesearch' }
        else { return }


    })
});

//20200522 wonjihoon 키값과 이름 저장
//20200602 wonjihoon 모듈 등록 권한 존재하지 않을 시 이전페이지
$(document).ready(function(){
    if(SValue != null){
        if(SValue.AUTH.indexOf('AUMOD0005') == -1){history.back(); alert('모듈 등록 권한이 존재하지 않습니다. 이전 페이지로 이동합니다.')}}
    document.getElementById('upload_file_user_key').value = SKey;
    document.getElementById("module_author").innerHTML = SValue.USER_NAME;

});

//20200522 wonjihoon 첨부파일 첨부 시 정보 표출
$(function () {
    $('#upload_file_file').change(function (e) {

        if(document.getElementById('upload_file_file').value != '') {
            var filesize = (document.getElementById('upload_file_file').files[0].size/1024).toFixed(3) +'KB';
            if(document.getElementById('upload_file_file').files[0].size >= 1024 * 1024){
                filesize = (document.getElementById('upload_file_file').files[0].size/1024/1024).toFixed(3) + 'MB';
            }
            $('#file_info').show();
            var strFile = '';
            strFile += document.getElementById('upload_file_file').files[0].name + '&nbsp; [용량: ' + filesize + ']';

            $("#file_span").html(strFile);
        }
    })

})

//20200529 wonjihoon input type='file' 을 버튼으로 대체
$(function () {
    $("#uploadbtn").click(function (e) {
            e.preventDefault();
            $('#upload_file_file').click();
    })
});

//20200529 wonjihoon X 버튼
$(function () {
    $("#xbtn").click(function () {
        var result = confirm('첨부한 파일을 취소하시겠습니까?');
        if(result) {
            $('#file_info').hide();
            $('#upload_file_file').val('');
        }
        else { return }
    })
});
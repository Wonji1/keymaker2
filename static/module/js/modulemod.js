//20200623 wonjihoon 인식모듈 수정 파일

//20200522 wonjihoon 수정페이지 상세정보 표출
//20200602 wonjihoon 수정 권한 존재하지 않을 시 이전페이지
//20200522 wonjihoon 모듈 수정 유효성 검사
//20200522 wonjihoon 파일없이 모듈수정
//20200522 wonjihoon 업로드 진행률
//20200522 wonjihoon 수정 취소 버튼
//20200522 wonjihoon X 버튼
//20200522 wonjihoon 첨부파일 첨부 시 정보 표출
//20200522 wonjihoon input type='file' 을 버튼으로 대체

document.write("<script src='/static/main/js/config.js'></script>");

//20200522 wonjihoon 수정페이지 상세정보 표출
//20200602 wonjihoon 수정 권한 존재하지 않을 시 이전페이지
$(document).ready(function () {
    if(SValue != null){//SValue --> config.js 파일에 있으며 session에 저장된 key에 대한 value 값이다 , AUKMOD0003은 인식모듈 수정 권한이다.
        if(SValue.AUTH.indexOf('AUMOD0003') == -1){history.back(); alert('모듈 수정 권한이 존재하지 않습니다. 이전 페이지로 이동합니다.')}}
    document.getElementById('upload_file_user_key').value = SKey;
    $.ajax({
        url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/get_module_info/' + SKey + '/LGMOD0003/' + document.getElementById("idx").value,
        type: 'post',
        success: function (data) {
            if (data.status == '401') {
                alert('접속 여부 확인 도중 DB 에러가 났습니다.');
                return
            }
            if (data.status == '402') {
                alert('인식모듈 수정을 요청했지만 작성한 사용자가 아니고 수정권한이 없습니다.');
                return
            }
            if (data.status == '403') {
                alert('인식모듈 정보를 불러오는 도중 DB 에러가 났습니다.');
                return
            }

            $("#existflag").val(data.data[0].FILE_EXIST_FLAG);
            $("#module_name").val(data.data[0].MODULE_NAME);
            $("#module_version").val(data.data[0].VERSION);
            $("#module_author").html(data.data[0].USER_NAME);
            $("#module_click").html(data.data[0].COUNT_CLICK);
            $("#module_time").html(data.data[0].DATE_REG + '&nbsp;&nbsp;&nbsp' + data.data[0].TIME_REG);

            var filesize = (data.data[0].FILE_SIZE / 1024).toFixed(3) + 'KB';
            if (data.data[0].FILE_SIZE >= 1024 * 1024) {
                filesize = (data.data[0].FILE_SIZE / 1024 / 1024).toFixed(3) + 'MB';
            }

            var strFile = ''; //파일 정보 담을 공간
            if (data.data[0].FILE_EXIST_FLAG == 'N') {
                strFile = '';
                $('#file_info').hide();
            } else {
                strFile += data.data[0].FILE_NAME_ORI + '&nbsp; [용량: ' + filesize + ']' +
                    '<span style="color: silver; font-size: 0.9em;">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;다운로드 : ' + data.data[0].COUNT_DOWN + '</span>';
            }
            $("#file_span").html(strFile);
            $("#module_memo").val(data.data[0].MEMO);

        },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            return
        }
    });

});

//20200522 wonjihoon 모듈 수정 유효성 검사
function formChk() {
    if (document.getElementById('upload_file_file').value != '') {
        document.getElementById('upload_file_file_name').value = document.getElementById('upload_file_file').files[0].name;
        document.getElementById('upload_file_file_size').value = document.getElementById('upload_file_file').files[0].size;
        if (check_db.test(document.getElementById('module_name')) || check_db.test(document.getElementById('module_version'))
            || check_db.test(document.getElementById('module_memo'))) {
            alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
            return false
        }
        if (document.getElementById('module_name').value == '' || document.getElementById('module_name').value.length > 30) {
            alert("모듈명을 30자 이내로 입력하세요!!");
            document.getElementById('module_name').focus();
            return false
        } else if (document.getElementById('module_version').value == '' || document.getElementById('module_version').value.length > 30) {
            alert("버전을 입력하세요!!");
            document.getElementById('module_version').focus();
            return false
        } else if (document.getElementById('upload_file_file_size').value > 500 * 1024 * 1024) {
            alert("파일을 500MB 이내로 첨부하세요!!");
            return false
        } else if (document.getElementById('module_memo').value == '' || document.getElementById('module_memo').value.length > 300) {
            alert("메모를 300자 이내로 입력하세요!!");
            document.getElementById('module_memo').focus();
            return false
        } else {
            $.ajax({
                url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/set_module_info/' + SKey + '/' + document.getElementById('idx').value + '/' + document.getElementById('module_name').value + '/'
                    + document.getElementById('module_version').value + '/' + document.getElementById('module_memo').value,
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
                        alert('작성자가 아니고 인식모듈 등록 권한이 존재하지 않습니다.');
                        return
                    }
                    if (data.status == '404') {
                        alert('인식모듈 정보를 불러오는 도중 DB 에러가 났습니다.');
                        return
                    }
                    if (data.status == '405') {
                        alert('입력값에서 DB 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.');
                        return
                    }
                    if (document.getElementById('existflag').value == 'Y' && document.getElementById('delapiflag').value == 'Y') {
                        $.ajax({
                            url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/del_file/' + SKey + '/LGMOD0004/' + document.getElementById('idx').value,
                            type: 'post',
                            async: false,
                            success: function (data) {
                                if (data.status == '400') {
                                    alert('파일이 제대로 입력되지 않았습니다.');
                                    return
                                }
                                if (data.status == '401') {
                                    alert('파일 업로드 도중 DB 에러가 났습니다.');
                                    return
                                }
                            },
                            error: function (request, status, error) {
                                alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                                return
                            }
                        });
                    }

                    document.getElementById('upload_file_index').value = document.getElementById('idx').value;
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

//20200522 wonjihoon 파일없이 모듈수정
$(function () {
    $("#mod_module2").click(function () {
        if (document.getElementById('upload_file_file').value == '') {
            if (check_db.test(document.getElementById('module_name')) || check_db.test(document.getElementById('module_version'))
                || check_db.test(document.getElementById('module_memo'))) {
                alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
                return false
            }
            if (document.getElementById('module_name').value == '' || document.getElementById('module_name').value.length > 30) {
                alert("모듈명을 30자 이내로 입력하세요!!");
                document.getElementById('module_name').focus();
                return
            } else if (document.getElementById('module_version').value == '' || document.getElementById('module_version').value.length > 30) {
                alert("버전을 입력하세요!!");
                document.getElementById('module_version').focus();
                return
            } else if (document.getElementById('module_memo').value == '' || document.getElementById('module_memo').value.length > 300) {
                alert("메모를 300자 이내로 입력하세요!!");
                document.getElementById('module_memo').focus();
                return
            }

            $.ajax({
                url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/set_module_info/' + SKey + '/' + document.getElementById('idx').value + '/' + document.getElementById('module_name').value + '/'
                    + document.getElementById('module_version').value + '/' + document.getElementById('module_memo').value,
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
                        alert('작성자가 아니고 인식모듈 등록 권한이 존재하지 않습니다.');
                        return
                    }
                    if (data.status == '404') {
                        alert('인식모듈 정보를 불러오는 도중 DB 에러가 났습니다.');
                        return
                    }
                    if (data.status == '405') {
                        alert('입력값에서 DB 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.');
                        return
                    }
                    if (document.getElementById('existflag').value == 'Y' && document.getElementById('delapiflag').value == 'Y') {
                        $.ajax({
                            url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/del_file/' + SKey + '/LGMOD0004/' + document.getElementById('idx').value,
                            type: 'post',
                            async: false,
                            success: function (data) {
                                if (data.status == '400') {
                                    alert('파일이 제대로 입력되지 않았습니다.');
                                    return
                                }
                                if (data.status == '401') {
                                    alert('파일 업로드 도중 DB 에러가 났습니다.');
                                    return
                                }
                            },
                            error: function (request, status, error) {
                                alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                                return
                            }
                        });
                    }
                    alert('수정되었습니다.');
                    location.href = '/moduledetail/' + document.getElementById('idx').value;
                },
                error: function (request, status, error) {
                    alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                    return
                }
            });
        }
    })
});


//20200522 wonjihoon 업로드 진행률
$(function () {
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
            alert('모듈이 수정되었습니다.');
            location.href = '/moduledetail/' + document.getElementById('upload_file_index').value;
        },
        error: function (e) {
            alert('모듈 수정에 실패하였습니다.');
            return
        }

    });

});

//20200522 wonjihoon 수정 취소 버튼
$(function () {
    $("#cancel_modmodule").click(function () {
        var result = confirm('수정을 취소하시겠습니까?');
        if (result) {
            location.href = '/moduledetail/' + document.getElementById('idx').value;
        } else {
            return
        }
    })
});

//20200522 wonjihoon X 버튼
$(function () {
    $("#xbtn").click(function () {
        var result = confirm('첨부한 파일을 삭제하시겠습니까?');
        if (result) {
            $('#file_info').hide();
            $('#upload_file_file').val('');
            $('#delapiflag').val('Y');
        } else {
            return
        }
    })
});

//20200522 wonjihoon 첨부파일 첨부 시 정보 표출
$(function () {
    $('#upload_file_file').change(function (e) {

        if (document.getElementById('upload_file_file').value != '') {
            var filesize = (document.getElementById('upload_file_file').files[0].size / 1024).toFixed(3) + 'KB';
            if (document.getElementById('upload_file_file').files[0].size >= 1024 * 1024) {
                filesize = (document.getElementById('upload_file_file').files[0].size / 1024 / 1024).toFixed(3) + 'MB';
            }
            $('#file_info').show();
            var strFile = ''; // 파일정보를 담는 공간
            strFile += document.getElementById('upload_file_file').files[0].name + '&nbsp; [용량: ' + filesize + ']';

            $("#file_span").html(strFile);
        }
    })

})

//20200522 wonjihoon input type='file' 을 버튼으로 대체
$(function () {
    $("#uploadbtn").click(function (e) {
        if (document.getElementById('existflag').value == 'Y' && document.getElementById('delapiflag').value == 'N') {
            var result = confirm('파일은 최대 1개 첨부 가능합니다. 기존에 첨부된 파일을 삭제하고 파일을 새로 첨부하시겠습니까?');
            if (result) {
                e.preventDefault();
                $('#upload_file_file').click();
            } else {
                return
            }
        } else {
            e.preventDefault();
            $('#upload_file_file').click();
        }
    })
});

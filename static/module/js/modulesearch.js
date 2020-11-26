//20200623 wonjihoon 인식모듈 조회 파일

//20200519 wonjihoon 등록버튼
//20200519 wonjihoon 검색버튼
//20205020 wonjihoon 이전 페이지 이동
//20200520 wonjihoon 다음 페이지 이동
//20200520 wonjihoon selectbox 클릭 이벤트
//20200520 wonjihoon 페이징 처리
//20200520 wonjihoon 화면 켜질때 모듈 리스트
//20200602 wonjihoon 모듈조회 권한이 존재하지 않을 시 이전 페이지로 이동

document.write("<script src='/static/main/js/config.js'></script>");

//20200519 wonjihoon 등록버튼
$(function () {
    $("#add_module").click(function () {
        location.href = '/moduleadd';

    })
});

//20200519 wonjihoon 검색버튼
$(function () {
    $("#search_module").click(function () {
        sessionStorage.removeItem("selectbox"); //페이지당 개수 session에 저장하는 key 삭제
        sessionStorage.removeItem("page"); // 현재 페이지 번호를 session에 저장하는 key 삭제
       var module_name  = document.getElementById('module_name').value;
       if(module_name == ""){
           module_name = 0;
       }
       else if(module_name.length > 20){
               alert('모듈명은 20자 이내로 검색해 주세요,');
               return
       }
       var module_author = document.getElementById('module_author').value;
        if(module_author == ""){
            module_author = 0;
        }
        else if(module_author.length > 20){
            alert('작성자는 20자 이내로 검색해 주세요,');
            return
        }
       var module_version = document.getElementById('module_version').value;
        if(module_version == ""){
            module_version = 0;
        }
        else if(module_version.length > 20){
            alert('모듈버전은 20자 이내로 검색해 주세요,');
            return
        }
       var module_memo = document.getElementById('module_memo').value;
        if(module_memo == ""){
            module_memo = 0;
        }
        else if(module_memo.length > 20){
            alert('모듈메모는 20자 이내로 검색해 주세요,');
            return
        }
       var sdate = document.getElementById('sdate').value;
        if(sdate == ""){
            sdate = 0;
        }
        else if (!datatimeRegexp.test(sdate)) {
            alert("날짜는 yyyy-mm-dd 형식으로 입력해주세요.");
            return
        }
       var edate = document.getElementById('edate').value;
        if(edate == ""){
            edate = 0;
        }
        else if (!datatimeRegexp.test(edate)) {
            alert("날짜는 yyyy-mm-dd 형식으로 입력해주세요.");
            return
        }

        if(sdate > edate){
            alert("등록일 시작 값이 등록일 끝 값보다 작게 설정해주세요.");
            return;
        }
        if(check_db.test(module_name) || check_db.test(module_author) || check_db.test(module_version) || check_db.test(module_memo)
            || check_db.test(sdate) || check_db.test(edate)){
            alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
            return false
        }
       var arr = {"pre": [module_name, module_author, module_version, module_memo, sdate, edate]};
       sessionStorage.setItem("modulesearch",JSON.stringify(arr));
       var parsearr = JSON.parse(sessionStorage.getItem("modulesearch")); // 검색값 세션에 저장


        $.ajax({
            url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_module_list/'+SKey+'/'+parsearr.pre[0] +'/' +parsearr.pre[1]+ '/'
            +parsearr.pre[2]+ '/' +parsearr.pre[3]+ '/'+parsearr.pre[4]+'/'+parsearr.pre[5]+'/1/10',
            type: 'post',
            success: function(data) {
                if(data.status == '201'){alert('결과값이 존재하지 않습니다.'); sessionStorage.removeItem("modulesearch"); return}
                if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
                if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
                if(data.status == '402'){alert('인식모듈 조회 권한이 존재하지 않습니다.'); return}
                if(data.status == '403'){alert('인식모듈 조회 도중 DB 에러가 났습니다.'); return}

                document.getElementById('total_module').innerHTML = data.data[0].TOTAL;
                var str = '';   //모듈 리스트를 담을 공간
                var str2 = '';  // 모듈이 있고 없고에 따라 아이콘을넣을 공간
                var str3 = '';  // 페이징 버튼들을 담을 공간
                var pagecount = data.data[0].TOTAL /10; // 페이지 개수 구하기
                if(pagecount == parseInt(pagecount)){
                    pagecount = pagecount ;
                }
                else{
                    pagecount = Math.floor(pagecount) +1;
                }

                for(var i =0; i< data.data.length; i++){
                    if(data.data[i].FILE_EXIST_FLAG == 'Y'){
                        str2 = '<img src="/static/module/img/icon_file.png">';
                    }else{
                        str2 = '';
                    }
                    if( sessionStorage.getItem("page") == null)
                        str += '<div class="item">' +
                            '<div class="num">'+(i +1) +'</div>' +
                            '<div class="name"><a style="font-size: 1em;" href="/moduledetail/'+data.data[i].IX_KMMITN_MODULEINFO+'">'+data.data[i].MODULE_NAME+'</a></div>' +
                            '<div class="version">'+data.data[i].VERSION+'</div>' +
                            '<div class="writer">'+data.data[i].USER_NAME+'</div>' +
                            '<div class="filecheck" >'+str2+'</div>' +
                            '<div class="date">'+data.data[i].DATE_REG+'</div>' +
                            '<div class="view">'+data.data[i].COUNT_CLICK+'</div> </div>'
                }
                $('#modulesearch_body').html(str);

                str3 +=  '<a class="bt first" onclick="goPage(1)">처음 페이지</a>' +
                    '<a class="bt prev" onclick="goPre()">이전 페이지</a>';
                for(var j=1; j <= pagecount ; j++)
                {
                    str3 +='<a class="num" onclick="goPage('+j+')">'+j+'</a>';
                }
                str3 += '<a class="bt next" onclick="goPro('+pagecount+')">다음 페이지</a>' +
                    '<a class="bt last" onclick="goPage('+pagecount+')">마지막 페이지</a>';
                $('#paging').html(str3);
            },
            error:function(request,status,error){
                alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
                return
            }

        });
    })
});

//20205020 wonjihoon 이전 페이지 이동
function goPre() {
    if(sessionStorage.getItem("page") == null || sessionStorage.getItem("page") == 1){
        goPage(1);
    }
    else{
        goPage(sessionStorage.getItem("page")-1);
    }
}

//20200520 wonjihoon 다음 페이지 이동
function goPro(pagecount) {
    if(sessionStorage.getItem("page") == null){
        goPage(2);
    }
    else if(sessionStorage.getItem("page") == pagecount){
        goPage(pagecount);
    }
    else{
        goPage(Number(sessionStorage.getItem("page"))+ 1);
    }
}

//20200520 wonjihoon selectbox 클릭 이벤트
function selectbox(n){

    sessionStorage.removeItem("page");
    sessionStorage.setItem("selectbox",n);
    var parsearr = JSON.parse(sessionStorage.getItem("modulesearch")); // 검색 결과 저장
    if(parsearr == null){
        parsearr = {"pre":[0,0,0,0,0,0]};
    }
    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_module_list/'+SKey+'/'+parsearr.pre[0] +'/' +parsearr.pre[1]+ '/'
            +parsearr.pre[2]+ '/' +parsearr.pre[3]+ '/'+parsearr.pre[4]+'/'+parsearr.pre[5]+'/1/'+sessionStorage.getItem("selectbox"),
        type: 'post',
        success: function(data) {
            if(data.status == '201'){alert('결과값이 존재하지 않습니다.'); return}
            if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
            if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
            if(data.status == '402'){alert('인식모듈 조회 권한이 존재하지 않습니다.'); return}
            if(data.status == '403'){alert('인식모듈 조회 도중 DB 에러가 났습니다.'); return}

            document.getElementById('total_module').innerHTML = data.data[0].TOTAL;

            var pagecount = data.data[0].TOTAL / sessionStorage.getItem("selectbox");
            if(pagecount == parseInt(pagecount)){
                pagecount = pagecount ;
            }
            else{
                pagecount = Math.floor(pagecount) +1;
            }

            var str = '';   //모듈 리스트를 담을 공간
            var str2 = '';  // 모듈이 있고 없고에 따라 아이콘을넣을 공간
            var str3 = '';  // 페이징 버튼들을 담을 공간
            for(var i =0; i< data.data.length; i++){
                if(data.data[i].FILE_EXIST_FLAG == 'Y'){
                    str2 = '<img src="/static/module/img/icon_file.png">';
                }
                else{
                    str2 = '';
                }
                str += '<div class="item">' +
                    '<div class="num">'+(i +1) +'</div>' +
                    '<div class="name"><a style="font-size: 1em;" href="/moduledetail/'+data.data[i].IX_KMMITN_MODULEINFO+'">'+data.data[i].MODULE_NAME+'</a></div>' +
                    '<div class="version">'+data.data[i].VERSION+'</div>' +
                    '<div class="writer">'+data.data[i].USER_NAME+'</div>' +
                    '<div class="filecheck" >'+str2+'</div>' +
                    '<div class="date">'+data.data[i].DATE_REG+'</div>' +
                    '<div class="view">'+data.data[i].COUNT_CLICK+'</div> </div>'
            }
            $('#modulesearch_body').html(str);

            str3 +=  '<a class="bt first" onclick="goPage(1)">처음 페이지</a>' +
                '<a class="bt prev" onclick="goPre()">이전 페이지</a>';
            for(var j=1; j <= pagecount ; j++)
            {
                str3 +='<a class="num" onclick="goPage('+j+')">'+j+'</a>';
            }
            str3 += '<a class="bt next" onclick="goPro('+pagecount+')">다음 페이지</a>' +
                '<a class="bt last" onclick="goPage('+pagecount+')">마지막 페이지</a>';
            $('#paging').html(str3);
        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }

    });
}

//20200520 wonjihoon 페이징 처리
function goPage(n){
    sessionStorage.setItem("page",n);
    var parsearr = JSON.parse(sessionStorage.getItem("modulesearch"));
    if(parsearr == null){
        parsearr = {"pre":[0,0,0,0,0,0]};
    }
    var selectval = sessionStorage.getItem("selectbox");
    if(selectval == null){
        selectval = 10;
    }
    var pageval = sessionStorage.getItem("page");
    if( pageval == null){
        pageval = 1;
    }
    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_module_list/'+SKey+'/'+parsearr.pre[0] +'/' +parsearr.pre[1]+ '/'
            +parsearr.pre[2]+ '/' +parsearr.pre[3]+ '/'+parsearr.pre[4]+'/'+parsearr.pre[5]+'/'+n+'/'+selectval,
        type: 'post',
        success: function(data) {
            if(data.status == '201'){alert('결과값이 존재하지 않습니다.'); return}
            if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
            if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
            if(data.status == '402'){alert('인식모듈 조회 권한이 존재하지 않습니다.'); return}
            if(data.status == '403'){alert('인식모듈 조회 도중 DB 에러가 났습니다.'); return}

            document.getElementById('total_module').innerHTML = data.data[0].TOTAL;

            var str = '';   //모듈 리스트를 담을 공간
            var str2 = '';  // 모듈이 있고 없고에 따라 아이콘을넣을 공간
            for(var i =0; i< data.data.length; i++){
                if(data.data[i].FILE_EXIST_FLAG == 'Y'){
                    str2 = '<img src="/static/module/img/icon_file.png">';
                }else{
                    str2 = '';
                }
                str += '<div class="item">' +
                    '<div class="num">'+((pageval-1)*selectval +i +1) +'</div>' +
                    '<div class="name"><a style="font-size: 1em;" href="/moduledetail/'+data.data[i].IX_KMMITN_MODULEINFO+'">'+data.data[i].MODULE_NAME+'</a></div>' +
                    '<div class="version">'+data.data[i].VERSION+'</div>' +
                    '<div class="writer">'+data.data[i].USER_NAME+'</div>' +
                    '<div class="filecheck" >'+str2+'</div>' +
                    '<div class="date">'+data.data[i].DATE_REG+'</div>' +
                    '<div class="view">'+data.data[i].COUNT_CLICK+'</div> </div>'
            }
            $('#modulesearch_body').html(str);

        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }

    });
}

//20200520 wonjihoon 화면 켜질때 모듈 리스트
//20200602 wonjihoon 모듈조회 권한이 존재하지 않을 시 이전 페이지로 이동
$(document).ready(function(){
    if(SValue != null){
        if(SValue.AUTH.indexOf('AUMOD0001') == -1){history.back(); alert('모듈 조회 권한이 존재하지 않습니다. 이전 페이지로 이동합니다.')}}
    if(SValue.AUTH.indexOf('AUMOD0005') != -1){
        $("#add_module").show();
    }
    var pageval = sessionStorage.getItem("page");
    if( pageval == null){
        pageval = 1;
    }
    var selectval = sessionStorage.getItem("selectbox");
    if(selectval == null){
        selectval = 10;
    }
    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_module_list/'+SKey+'/0/0/0/0/0/0/'+pageval+'/'+ selectval,
        type: 'post',
        success: function(data) {
            if(data.status == '201'){alert('결과값이 존재하지 않습니다.'); return}
            if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
            if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
            if(data.status == '402'){alert('인식모듈 조회 권한이 존재하지 않습니다.'); return}
            if(data.status == '403'){alert('인식모듈 조회 도중 DB 에러가 났습니다.'); return}

            document.getElementById('total_module').innerHTML = data.data[0].TOTAL;

            var pagecount = data.data[0].TOTAL /10;
            if(pagecount == parseInt(pagecount)){
                pagecount = pagecount ;
            }
            else{
                pagecount = Math.floor(pagecount) +1;
            }
            var selectval = sessionStorage.getItem("selectbox");
            if(selectval == null){
                selectval = 10;
            }
            var pageval = sessionStorage.getItem("page");
            if( pageval == null){
                pageval = 1;
            }
            var str = '';   //모듈 리스트를 담을 공간
            var str2 = '';  // 모듈이 있고 없고에 따라 아이콘을넣을 공간
            var str3 = '';  // 페이징 버튼들을 담을 공간
            for(var i =0; i< data.data.length; i++){
                if(data.data[i].FILE_EXIST_FLAG == 'Y'){
                    str2 = '<img src="/static/module/img/icon_file.png">';
                }else{
                    str2 = '';
                }

                str += '<div class="item">' +
                    '<div class="num">'+((pageval-1)*selectval +i +1) +'</div>' +
                    '<div class="name"><a style="font-size: 1em;" href="/moduledetail/'+data.data[i].IX_KMMITN_MODULEINFO+'">'+data.data[i].MODULE_NAME+'</a></div>' +
                    '<div class="version">'+data.data[i].VERSION+'</div>' +
                    '<div class="writer">'+data.data[i].USER_NAME+'</div>' +
                    '<div class="filecheck" >'+str2+'</div>' +
                    '<div class="date">'+data.data[i].DATE_REG+'</div>' +
                    '<div class="view">'+data.data[i].COUNT_CLICK+'</div> </div>'
            }
            $('#modulesearch_body').html(str);

            str3 +=  '<a class="bt first" onclick="goPage(1)">처음 페이지</a>' +
                    '<a class="bt prev" onclick="goPre()" >이전 페이지</a>';
            for(var j=1; j <= pagecount ; j++)
            {
             str3 +='<a class="num" onclick="goPage('+j+')">'+j+'</a>';
            }
            str3 += '<a class="bt next" onclick="goPro('+pagecount+')">다음 페이지</a>' +
                '<a class="bt last" onclick="goPage('+pagecount+')">마지막 페이지</a>';
            $('#paging').html(str3);

        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }

    });

});
//20200623 wonjihoon 인식키 조회 파일

//20200528 wonjihoon 검색버튼
//20205020 wonjihoon 이전 페이지 이동
//20200520 wonjihoon 다음 페이지 이동
//20200520 wonjihoon selectbox 클릭 이벤트
//20200520 wonjihoon 페이징 처리
//20200520 wonjihoon 화면 켜질때 인증키 리스트
//20200602 wonjihoon 권한 없을 시 이전 페이지 이동

document.write("<script src='/static/main/js/config.js'></script>");

//20200528 wonjihoon 검색버튼
$(function () {
    $("#searchbtn").click(function () {
        sessionStorage.removeItem("selectbox");
        sessionStorage.removeItem("page"); //검색버튼 클릭 시 그 전에 저장된 selectbox의 값과 page의 값을 삭제
        var key_name  = document.getElementById('key_name').value;
        if(key_name == ""){
            key_name = 0;
        }
        else if(key_name.length > 20){
            alert('이름은 20자 이내로 검색해 주세요,');
            return
        }
        var key_loc = document.getElementById('key_loc').value;
        if(key_loc == ""){
            key_loc = 0;
        }
        else if(key_loc.length > 20){
            alert('발급장소는 20자 이내로 검색해 주세요,');
            return
        }
        var key_id = document.getElementById('key_id').value;
        if(key_id == ""){
            key_id = 0;
        }
        else if(key_id.length > 20){
            alert('ID는 20자 이내로 검색해 주세요,');
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
        if(check_db.test(key_name) || check_db.test(key_loc) || check_db.test(key_id) || check_db.test(sdate) || check_db.test(edate)){
            alert("입력창에 '#', '\\', '?', '/', '%', '_' 문자를 넣지 마세요.");
            return false
        }
        var arr = {"pre": [key_name, key_loc, key_id, sdate, edate]};
        sessionStorage.setItem("keysearch",JSON.stringify(arr));
        var parsearr = JSON.parse(sessionStorage.getItem("keysearch"));


        $.ajax({
            url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_key_list/'+SKey+'/'+parsearr.pre[0] +'/' +parsearr.pre[1]+ '/'
                +parsearr.pre[2]+ '/' +parsearr.pre[3]+ '/'+parsearr.pre[4]+ '/1/10',
            type: 'post',
            success: function(data) {
                if(data.status == '201'){alert('결과값이 존재하지 않습니다.'); sessionStorage.removeItem("keysearch"); return}
                if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
                if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
                if(data.status == '402'){alert('인식키 리스트 조회 도중 DB 에러가 났습니다.'); return}
                if(data.status == '403'){alert('입력값에서 디비 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.'); return}
                if(data.status == '404'){alert('인식키 조회 권한이 존재하지 않습니다.'); return}

                document.getElementById('total_key').innerHTML = data.data[0].TOTAL;


                var str = ''; // 인식키 조회 리스트 담을 공간
                var str3 = ''; //페이징 버튼들 담을 공간
                var pagecount = data.data[0].TOTAL /10; //페이지 개수 초기값
                if(pagecount == parseInt(pagecount)){
                    pagecount = pagecount;
                }
                else{
                    pagecount = Math.floor(pagecount) +1;
                }


                for(var i =0; i< data.data.length; i++){
                    if( sessionStorage.getItem("page") == null)
                        str += '<div class="item">' +
                            '<div class="num">'+(i +1) +'</div>' +
                            '<div class="name"><a style="font-size: 1em" href="/keydetail/'+data.data[i].PK_KMKITN_KEYINFO+'" onclick="window.open(this.href,\'\',\'top=130, left=10, width=500, height=420, status=no, menubar=no, toolbar=no, resizable=no, titlebar=no, location=no\');return false;">'+data.data[i].USER_NAME+'</a></div>' +
                            '<div class="id">'+data.data[i].result_data_1+'</div>' +
                            '<div class="place">'+data.data[i].FULL_ADDRESS+'</div>' +
                            '<div class="date">'+data.data[i].DATE+'</div>' +
                            '<div class="logcheck">'+data.data[i].LOGIN+'</div> </div>'
                }
                $('#key_body').html(str);

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
    var parsearr = JSON.parse(sessionStorage.getItem("keysearch"));
    if(parsearr == null){
        parsearr = {"pre":[0,0,0,0,0]};
    }
    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_key_list/'+SKey+'/'+parsearr.pre[0] +'/' +parsearr.pre[1]+ '/'
            +parsearr.pre[2]+ '/' +parsearr.pre[3]+ '/'+parsearr.pre[4]+'/1/'+sessionStorage.getItem("selectbox"),
        type: 'post',
        success: function(data) {
            console.log(data);
            if(data.status == '201'){alert('결과값이 존재하지 않습니다.'); sessionStorage.removeItem("keysearch"); return}
            if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
            if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
            if(data.status == '402'){alert('인식키 리스트 조회 도중 DB 에러가 났습니다.'); return}
            if(data.status == '403'){alert('입력값에서 디비 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.'); return}
            if(data.status == '404'){alert('인식키 조회 권한이 존재하지 않습니다.'); return}

            document.getElementById('total_key').innerHTML = data.data[0].TOTAL;

            var pagecount = data.data[0].TOTAL / sessionStorage.getItem("selectbox"); //페이지 개수 계산
            if(pagecount == parseInt(pagecount)){
                pagecount = pagecount ;
            }
            else{
                pagecount = Math.floor(pagecount) +1;
            }

            var str = ''; //인식키 조회 리스트 담을 공간
            var str3 = ''; // 페이징 버튼들 담을 공간
            for(var i =0; i< data.data.length; i++){
                str += '<div class="item">' +
                    '<div class="num">'+(i +1) +'</div>' +
                    '<div class="name"><a style="font-size: 1em" href="/keydetail/'+data.data[i].PK_KMKITN_KEYINFO+'" onclick="window.open(this.href,\'\',\'top=130, left=10, width=500, height=420, status=no, menubar=no, toolbar=no, resizable=no, titlebar=no, location=no\');return false;">'+data.data[i].USER_NAME+'</a></div>' +
                    '<div class="id">'+data.data[i].result_data_1+'</div>' +
                    '<div class="place">'+data.data[i].FULL_ADDRESS+'</div>' +
                    '<div class="date">'+data.data[i].DATE+'</div>' +
                    '<div class="logcheck">'+data.data[i].LOGIN+'</div> </div>'
            }
            $('#key_body').html(str);

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
    var parsearr = JSON.parse(sessionStorage.getItem("keysearch"));
    if(parsearr == null){
        parsearr = {"pre":[0,0,0,0,0]};
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
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_key_list/'+SKey+'/'+parsearr.pre[0] +'/' +parsearr.pre[1]+ '/'
            +parsearr.pre[2]+ '/' +parsearr.pre[3]+ '/'+parsearr.pre[4]+'/'+n+'/'+selectval,
        type: 'post',
        success: function(data) {
            if(data.status == '201'){alert('결과값이 존재하지 않습니다.'); sessionStorage.removeItem("keysearch"); return}
            if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
            if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
            if(data.status == '402'){alert('인식키 리스트 조회 도중 DB 에러가 났습니다.'); return}
            if(data.status == '403'){alert('입력값에서 디비 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.'); return}
            if(data.status == '404'){alert('인식키 조회 권한이 존재하지 않습니다.'); return}

            document.getElementById('total_key').innerHTML = data.data[0].TOTAL;

            var str = ''; // 인식키 조회 리스트 담을 공간
            for(var i =0; i< data.data.length; i++){
                str += '<div class="item">' +
                    '<div class="num">'+((pageval-1)*selectval +i +1) +'</div>' +
                    '<div class="name"><a style="font-size: 1em" href="/keydetail/'+data.data[i].PK_KMKITN_KEYINFO+'" onclick="window.open(this.href,\'\',\'top=130, left=10, width=500, height=420, status=no, menubar=no, toolbar=no, resizable=no, titlebar=no, location=no\');return false;">'+data.data[i].USER_NAME+'</a></div>' +
                    '<div class="id">'+data.data[i].result_data_1+'</div>' +
                    '<div class="place">'+data.data[i].FULL_ADDRESS+'</div>' +
                    '<div class="date">'+data.data[i].DATE+'</div>' +
                    '<div class="logcheck">'+data.data[i].LOGIN+'</div> </div>'
            }
            $('#key_body').html(str);

        },
        error:function(request,status,error){
            alert("code:"+request.status+"\n"+"message:"+request.responseText+"\n"+"error:"+error);
            return
        }

    });
}

//20200520 wonjihoon 화면 켜질때 인증키 리스트
//20200602 wonjihoon 권한 없을 시 이전 페이지 이동
$(document).ready(function(){
    if(SValue !=null){
    if(SValue.AUTH.indexOf('AUKEY0003') == -1){history.back(); alert('인식키 조회 권한이 존재하지 않습니다. 이전 페이지로 이동합니다.')}}
    var pageval = sessionStorage.getItem("page");
    if( pageval == null){
        pageval = 1;
    }
    var selectval = sessionStorage.getItem("selectbox");
    if(selectval == null){
        selectval = 10; //페이지당 개수 초기값 10개
    }
    $.ajax({
        url: apiProtocol+'://'+apiAdress+':'+apiPort+'/api/get_key_list/'+SKey+'/0/0/0/0/0/'+pageval+'/'+ selectval,
        type: 'post',
        success: function(data) {
            if(data.status == '201'){alert('결과값이 존재하지 않습니다.'); sessionStorage.removeItem("keysearch"); return}
            if(data.status == '400'){alert('접속해 있는 사용자가 아닙니다.'); return}
            if(data.status == '401'){alert('접속 여부 확인 도중 DB 에러가 났습니다.'); return}
            if(data.status == '402'){alert('인식키 리스트 조회 도중 DB 에러가 났습니다.'); return}
            if(data.status == '403'){alert('입력값에서 디비 또는 API 파라미터에 입력할 수 없는 특수문자가 포함되어 있습니다.'); return}
            if(data.status == '404'){alert('인식키 조회 권한이 존재하지 않습니다.'); return}

            document.getElementById('total_key').innerHTML = data.data[0].TOTAL;

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
            var str = ''; //인식키 조회 리스트 담을 공간
            var str3 = ''; // 페이징 처리 버튼 담을 공간
            for(var i =0; i< data.data.length; i++){
                str += '<div class="item">' +
                    '<div class="num">'+((pageval-1)*selectval +i +1) +'</div>' +
                    '<div class="name"><a style="font-size: 1em" href="/keydetail/'+data.data[i].PK_KMKITN_KEYINFO+'" onclick="window.open(this.href,\'\',\'top=130, left=10, width=500, height=420, status=no, menubar=no, toolbar=no, resizable=no, titlebar=no, location=no\');return false;">'+data.data[i].USER_NAME+'</a></div>' +
                    '<div class="id">'+data.data[i].result_data_1+'</div>' +
                    '<div class="place">'+data.data[i].FULL_ADDRESS+'</div>' +
                    '<div class="date">'+data.data[i].DATE+'</div>' +
                    '<div class="logcheck">'+data.data[i].LOGIN+'</div> </div>'
            }
            document.getElementById('key_body').innerHTML = str;

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
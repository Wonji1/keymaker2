document.write("<script src='/static/main/js/config.js'></script>");
//var timeStamp =  Math.floor(+new Date).toString();
//var accessKey = "Rq6GcpUu78vcmh6Zk3s0";                           // access key id (from portal or sub account)
//var secretKey = "FYzYAtDvRE2tDfvgnuD8FyPgiUrcw1AK64tego55";        // secret key (from portal or sub account)
//function makeSignature() {
//    var space = " ";                // one space
//    var newLine = "\n";                // new line
//    var method = "GET";                // method
//    var url = "https://geolocation.apigw.ntruss.com/geolocation/v2/geoLocation?ip=220.118.97.215&ext=t&responseFormatType=json";    // url (include query string)
//    var timestamp = timeStamp;            // current timestamp (epoch)
//
//
//
//    var hmac = CryptoJS.algo.HMAC.create(CryptoJS.algo.SHA256, secretKey);
//    hmac.update(method);
//    hmac.update(space);
//    hmac.update(url);
//    hmac.update(newLine);
//    hmac.update(timestamp);
//    hmac.update(newLine);
//    hmac.update(accessKey);
//
//    var hash = hmac.finalize();
//
//    return hash.toString(CryptoJS.enc.Base64);
//}

// function getLocation() {
//     if (navigator.geolocation) { // GeoLocation을 지원하면
//         navigator.geolocation.getCurrentPosition(function (position) {
//             $('#geo').html('위도 ' + position.coords.latitude + ' 경도' + position.coords.longitude);
//             $.ajax({
//                 url: 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + position.coords.latitude + ',' + position.coords.longitude + '&language=ko&key=AIzaSyBJAmvAImwegVT9nzZqLxAcxCowrkKzX48',
//                 type: 'POST',
//                 success: function (data) {
//                     $('#loc').html('위치 ' + data.results[1].formatted_address);
//                 },
//                 error: function (request, status, error) {
//                     alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
//                     return
//                 }
//             })
//         }, function (error) {
//             console.error(error);
//         }, {
//             enableHighAccuracy: false,
//             maximumAge: 0,
//             timeout: Infinity
//         });
//     } else {
//         alert('Geolocation을 지원하지 않습니다');
//     }
// }

function getLocation() {
    $.ajax({
        url: 'https://api.ip.pe.kr/json/',
        type: 'get',
        async: false,
        success: function (data) {
            $.ajax({
                url: apiProtocol + '://' + apiAdress + ':' + apiPort + '/api/get_loc_info/'+ data.ip,
                type: 'post',
                async: false,
                success: function (data) {
                    console.log(data);
                },
                error: function (request, status, error) {
                    alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
                    return
                }
            })
        },
        error: function (request, status, error) {
            alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
            return
        }
    })}
$(document).ready(function () {
    getLocation();
//    $.ajax({
//        url: 'https://api.ip.pe.kr/',
//        type: 'GET',
//        success: function (data) {
//            console.log(data);
//        },
//        error: function (data) {
//            console.log(data);
//        }
//    });
//    var ms = makeSignature();
//    console.log(ms);
    // $.ajax({
    //     url: 'https://geolocation.apigw.ntruss.com/geolocation/v2/geoLocation',
    //     type: 'GET',
    //     data: {
    //         ip: '220.118.97.215',
    //         ext: 't',
    //         responseFormatType: 'json'
    //     },
    //     beforeSend: function (xhr) {
    //         xhr.setRequestHeader('x-ncp-apigw-timestamp', timeStamp);
    //         xhr.setRequestHeader('x-ncp-iam-access-key', accessKey);
    //         xhr.setRequestHeader('x-ncp-apigw-signature-v2', ms);
    //     },
    //     success: function (data) {
    //         console.log(data);
    //     },
    //     error: function (data) {
    //         console.log(data);
    //     }
    // })
})

//06890162
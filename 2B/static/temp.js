

function jsts() {
    alert('asfdds');
    var xmlHttp = new XMLHttpRequest();       // XMLHttpRequest 객체를 생성함.

xmlHttp.onreadystatechange = function() { // onreadystatechange 이벤트 핸들러를 작성함.

    // 서버상에 문서가 존재하고 요청한 데이터의 처리가 완료되어 응답할 준비가 완료되었을 때

    if(this.status == 200 && this.readyState == this.DONE) {

        // 요청한 데이터를 문자열로 반환함.
        var i = xmlHttp.responseText;
        var j = JSON.parse(i);
        alert(j['namedata']);
        

    }

};

xmlHttp.open("GET", "/js", true);

xmlHttp.send();
}
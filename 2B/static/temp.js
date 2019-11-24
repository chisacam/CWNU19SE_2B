var i, j, namedataJson, geodataJson;



function jsts() {

  var mapContainer = document.getElementById('maps'), mapOption = {
    center: new kakao.maps.LatLng(myLat, myLong),
    level: 3
  };
  var map = new kakao.maps.Map(mapContainer, mapOption);
  var imageSrc = "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
  var imageSize = new kakao.maps.Size(30, 40);
  var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

  var marker = new kakao.maps.Marker({
    map: map,
    position: new kakao.maps.LatLng(myLat, myLong),
    image: markerImage
  });

  var control = new kakao.maps.ZoomControl();
  map.addControl(control, kakao.maps.ControlPosition.TOPRIGHT);


// 여기까지 무조건 옴
  var xmlHttp = new XMLHttpRequest();       // XMLHttpRequest 객체를 생성함.
  xmlHttp.onreadystatechange = function () { // onreadystatechange 이벤트 핸들러를 작성함.
    // 서버상에 문서가 존재하고 요청한 데이터의 처리가 완료되어 응답할 준비가 완료되었을 때
    if (this.status == 200 && this.readyState == this.DONE) {
      // 요청한 데이터를 문자열로 반환함.
      i = xmlHttp.responseText;
      j = JSON.parse(i);
      namedataJson = JSON.parse(j['namedata']);
      geodataJson = JSON.parse(j['geodata']);
      //alert(geodataJson[0]);
      //alert(namedataJson[0]);

      var positions = new Array();
      var title_latlng = new Object();
      
    
      //alert(1);
      for (var k = 0; k < 277; k++) {
        title_latlng["title"] = namedataJson[k];
        title_latlng["latlng"] = new kakao.maps.LatLng(geodataJson[k]);
        positions.push(title_latlng);
        document.write(title_latlng["latlng"]);
      }
      //alert(2);
      //alert(positions[0].title);
      //alert(positions[0].latlng);
      //alert(positions.length);
      //// OK 

      for (var i = 0; i < positions.length; i++) {
        var imageSize = new kakao.maps.Size(24, 35);
        var marker = new kakao.maps.Marker({
          map: map,
          position: positions[positions.length-i-1].latlng,
          title: positions[positions.length-i-1].title
        });
      }
      marker.setMap(map);
      alert(3);
    }
  }
  xmlHttp.open("GET", "/js", true);
  xmlHttp.send();
}

function departclick() {

  document.getElementById("sel").value = "depart";

};

function destclick() {
  document.getElementById("sel").value="dest";
};

function swaps() {
  var tempName = document.getElementById("departures").value;
  var tempLat = document.getElementById("departLat").value;
  var tempLong = document.getElementById("departLong").value;
  document.getElementById("departures").value = document.getElementById("destinations").value;
  document.getElementById("departLat").value = document.getElementById("destLat").value;
  document.getElementById("departLong").value = document.getElementById("destLong").value;
  document.getElementById("destinations").value = tempName;
  document.getElementById("destLat").value = tempLat;
  document.getElementById("destLong").value = tempLong;
  

};
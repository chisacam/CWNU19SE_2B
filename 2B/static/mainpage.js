// 사용자가 지도 중앙으로 오도록 위치 설정
var myLat;
var myLong;

// 위를 참고해 창이 켜지면 맵과 현재 위치를 로드

window.onload = () => {
  // Load as default
  myLat = 35.228002;
  myLong = 128.681816;

  var mapContainer = document.getElementById('maps'), mapOption = {
    center: new kakao.maps.LatLng(myLat, myLong),
    level: 3
  };

  var map = new kakao.maps.Map(mapContainer, mapOption);
  var imageSrc = "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";
  var imageSize = new kakao.maps.Size(30, 40);
  var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);
  // default marker
  var cenMarker = new kakao.maps.Marker({
    map: map,
    position: new kakao.maps.LatLng(myLat, myLong),
    image: markerImage,
    clickable: true
  });

  var control = new kakao.maps.ZoomControl();
  map.addControl(control, kakao.maps.ControlPosition.TOPRIGHT);

  // navigator.geolocation.getCurrentPosition(successGps, errorGps, opt);
  userLoc();
  function userLoc() {
    navigator.geolocation.getCurrentPosition(function (position) {
      // erase default
      cenMarker.setMap(null);

      myLat = position.coords.latitude;
      myLong = position.coords.longitude;
      // new center marker
      cenMarker = new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(myLat, myLong),
        image: markerImage,
        clickable: true
      });
      var moveCen = new kakao.maps.LatLng(myLat, myLong);
      map.setCenter(moveCen);
    });
  }
  // Go Center as GPS
  var gpsButton = document.getElementById('mapGpsButton');
  gpsButton.addEventListener('click', () => {
    if(navigator.geolocation){
      var moveCen = new kakao.maps.LatLng(myLat, myLong);
      map.setCenter(moveCen);
    }
    else{
      alert('GPS의 사용여부를 확인해주세요!')
    }
  });

  // All Markers
  var xmlHttp = new XMLHttpRequest();       // XMLHttpRequest 객체를 생성함.
  xmlHttp.onreadystatechange = function () { // onreadystatechange 이벤트 핸들러를 작성함.
    // 서버상에 문서가 존재하고 요청한 데이터의 처리가 완료되어 응답할 준비가 완료되었을 때
    if (this.status == 200 && this.readyState == this.DONE) {
      // 요청한 데이터를 문자열로 반환함.
      i = xmlHttp.responseText;
      j = JSON.parse(i);
      namedataJson = JSON.parse(j['namedata']);
      geodataJson = JSON.parse(j['geodata']);

      var positions = new Array();
      var title_latlng = new Object();

      for (var k = 0; k < 277; k++) {
        title_latlng.title = namedataJson[k];
        title_latlng.latlng = geodataJson[k];
        positions.push(JSON.stringify(title_latlng)); // 인덱스 역순으로 push
      }

      var markers = [];
      for (var i = 0; i < positions.length; i++) {
        var mPos = new kakao.maps.LatLng(JSON.parse(positions[i]).latlng[0], JSON.parse(positions[i]).latlng[1]);
        var marker = new kakao.maps.Marker({
          position: mPos,
          clickable: true
        });
        markers.push(marker);
      }

      showAll(markers, map);

      function showAll(markers, map) {
        for (var q = 0; q < 277; q++) {
          markers[q].setMap(map);
        }
      }
    }
  }
  xmlHttp.open("GET", "/js", true);
  xmlHttp.send();
}

function departclick() {
  document.getElementById("sel").value = "depart";

  document.getElementById('hiddenuserLat').value = myLat;
  document.getElementById('hiddenuserLong').value = myLong;
};

function destclick() {
  document.getElementById("sel").value = "dest";
  
  document.getElementById('hiddenuserLat').value = myLat;
  document.getElementById('hiddenuserLong').value = myLong;
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

// 누비자 선택 화면으로 현재 위도/경도를 넘긴다
function gpsData(target){
  // Get html's className
  var className = target.className;
  // and set location data
  document.getElementsByClassName(className)[0].value = "현재 위치";
  document.getElementsByClassName(className)[1].value = myLat;
  document.getElementsByClassName(className)[2].value = myLong;  
}


// 사용자가 지도 중앙으로 오도록 위치 설정
var myLat;
var myLong;
var gpsFlag = false;

// 위를 참고해 창이 켜지면 맵과 현재 위치를 로드
// 별모양 마커, 일반은 marker에서 image를 제거
var imageSrc = "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png";

window.onload = () => {
    navigator.geolocation.getCurrentPosition(function(position) {
        if(navigator.geolocation){
             myLat = position.coords.latitude;
             myLong = position.coords.latitude;
             gpsFlag = true;
         } else {
                alert('GPS를 사용할 수 없습니다.')
           }
        });
        

    // Default: 창원시청
    if (gpsFlag === false) {
        myLat = 35.228002;
        myLong = 128.681816;
        alert('GPS를 이용하지 않아 기본값을 사용합니다.')
    }

    var mapContainer = document.getElementById('maps'), mapOption = {
        center : new kakao.maps.LatLng(myLat, myLong),
        level : 3
    };
    var map = new kakao.maps.Map(mapContainer, mapOption);

    var imageSize = new kakao.maps.Size(24, 35);
    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize);

    var marker = new kakao.maps.Marker({
        map: map,
        position: new kakao.maps.LatLng(myLat, myLong),
        image: markerImage
    });
}

////
// Get GPS location
////

/* GPS검색을 이용할 때 사용해야함

var gps = document.getElementById('gps');

gps.addEventListener('click', function(){
    navigator.geolocation.getCurrentPosition(function(position) {
        if(navigator.geolocation){
            myLat = position.coords.latitude;
            myLong = position.coords.latitude;
        } else {
            alert('GPS를 사용할 수 없습니다.')
        }
      });
});
*/


////
// Set all terminal markers
////

/* position 형식은 다음을 따름
[
    {
        title: '카카오',
        latlng: new kakao.maps.LatLng(33.450705, 126.570677)
    },
    {
        title: '네오호수',
        latlng: new kakao.maps.LatLng(33.450936, 126.569477)
    },
    {
        title: '우리집',
        latlng: new kakao.maps.LatLng(33.450879, 126.569940)
    }
];

*/
var positions = [

];

for (var i = 0; i < positions.length; i ++) {
    var imageSize = new kakao.maps.Size(24, 35);
    var marker = new kakao.maps.Marker({
        map: map,
        position: positions[i].latlng,
        title : positions[i].title,
    });
}
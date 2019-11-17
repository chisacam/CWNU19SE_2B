
var mapContainer = document.getElementById('maps'), mapOption = {
    center : new kakao.maps.LatLng(35.228002, 128.681816),
    level : 3
};

var map = new kakao.maps.Map(mapContainer, mapOption);

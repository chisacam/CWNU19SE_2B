var positions = [];

// 별모양 마커
// var imageSrc = "http://t1.daumcdn.net/localimg/localimages/07/mapapidoc/markerStar.png"; 
    
for (var i = 0; i < positions.length; i ++) {
    
    var imageSize = new kakao.maps.Size(24, 35);   
    var marker = new kakao.maps.Marker({
        map: map,
        position: positions[i].latlng,
        title : positions[i].title,
    });
}

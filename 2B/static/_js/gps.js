////
// GPS
////

let myLat, myLong; // User's Latitude and Longtitude 
let gps = document.getElementById('gps');

gps.addEventListener('click', function(){
    navigator.geolocation.getCurrentPosition(function(position) {
        if(navigator.geolocation){
            //show_loc(position.coords.latitude, position.coords.longitude);
            myLat = position.coords.latitude;
            myLong = position.coords.latitude;
        } else {
            alert('GPS를 사용할 수 없습니다.')
        }
      });
});

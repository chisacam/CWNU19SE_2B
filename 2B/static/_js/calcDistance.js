/*
X = ( cos( 위도#1 ) * 6400 * 2 * 3.14 / 360 ) * | 경도#1 - 경도#2 |
Y = 111 * | 위도#1 - 위도#2 |
D = √ ( X² + Y² )
*/

let tempLong, tempLat;

let X = (Math.cos(myLat) * 6400 * 2 * 3.14 / 360) * Math.abs(myLong - tempLong);
let Y = 111 * Math.abs(MyLat - tempLat);
let D = Math.sqrt(X * X + Y * Y)
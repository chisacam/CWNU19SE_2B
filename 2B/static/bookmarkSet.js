function bmStateSet(event) {
  // 별, 안 별
    document.getElementById('chch').value = "true";
    event.src = "/static/icon/star_empty.svg"
}

function setLocationAsBM(event) {
    var temp = document.getElementsByClassName(event.className);
        document.getElementById('selname').value = temp[0];
        document.getElementById('selX').value = temp[1];
        document.getElementById('selY').value = temp[2];

}


function setLocationAsR(event) {
    var temp = document.getElementsByClassName(event.className);
        document.getElementById('selname').value = temp[2];
        document.getElementById('selX').value = temp[3];
        document.getElementById('selY').value = temp[4];

}

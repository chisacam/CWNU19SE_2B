function bmStateSet(event) {
  // 별, 안 별
    document.getElementById('chch').value = "true";
    event.src = "/static/icon/star_empty.svg"
}

function setLocationAsBM(event) {
    var temp = document.getElementsByClassName(event.className);
        document.getElementById('selectedName').value = temp[0].value;
        document.getElementById('selectedX').value = temp[1].value;
        document.getElementById('selectedY').value = temp[2].value;
}


function setLocationAsR(event) {
    var temp = document.getElementsByClassName(event.className);
        document.getElementById('selname').value = temp[2];
        document.getElementById('selX').value = temp[3];
        document.getElementById('selY').value = temp[4];

}

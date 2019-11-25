function bmStateSet(event) {
  // 별, 안 별
    alert('asdf');
    document.getElementById('chch').value = "true";
    event.src = "/static/icon/star_empty.svg"
}

function setLocationAsBM(event) {
    var temp = document.getElementsByClassName(event.className);
    alert(temp[0].value);
    alert(temp[1].value);
}


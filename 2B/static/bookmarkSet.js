function bmStateSet(event) {
  // 별, 안 별
    alert('asdf');
    document.getElementById('chch').value = "true";
    event.src = "/static/icon/star_empty.svg"
}

function setLocationAsBM() {
  // 북마크를 위치로 설정
}

function setBM() {
  // bmStateSet 이후 별이 있는 데이터만 날려서 쿠키에 저장
}

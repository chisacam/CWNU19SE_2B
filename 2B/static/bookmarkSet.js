/*
    1. 검색기록은 리스트형태로 나타나며 최근기록, 북마크를 사용자가 가장 최근에 선택한 항목을 상단으로 정렬한다.
      - 북마크는 별 아이콘이 노란색, 최근기록은 빈 별이다. 이는 검색기록에서 변수 1개로 제어한다.
    2. 검색기록에서 최근기록의 별을 클릭하면 별 아이콘이 노란색으로 바뀌고 다른 페이지(검색을 수행하거나 북마크 목록)으로 이동하면 추가되어야한다.
      - 북마크의 순서는 검색기록과 같이 최근 등록한 북마크가 상단에 위치한다.
    3. 검색기록에서 북마크로 등록할 때에는 넘겨주었던 인덱스를 참고하여 해당 데이터를 북마크에도 복사하여 저장한다.
*/

function setLocationAsBM(event) {
  var temp = document.getElementsByClassName(event.className);
  document.getElementById('selectedName').value = temp[0].value;
  document.getElementById('selectedX').value = temp[1].value;
  document.getElementById('selectedY').value = temp[2].value;
}

function setLocationAsR(event) {
  var temp = document.getElementsByClassName(event.classList[1]);
  document.getElementById('selectedName').value = temp[2].value;
  document.getElementById('selectedX').value = temp[4].value;
  document.getElementById('selectedY').value = temp[3].value;
}

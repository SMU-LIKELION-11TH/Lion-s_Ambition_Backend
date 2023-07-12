/*
const button = document.querySelector('.modal');
  const btnOpenPopup = document.getElementById('add-btn');
  const btnClosePopup = document.getElementById("close-btn");

  btnOpenPopup.addEventListener('click', () => {
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
  });

  btnClosePopup.addEventListener('click', () => {
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
  });

*/

const modal = document.getElementById("modal-wrap");
const openModalBtn = document.querySelectorAll(".ordernumber-btn");
const openModalCard = document.getElementById("card-item");
const closeModalBtn = document.getElementById("close-btn");

// // 모달창 열기
// openModalBtn.addEventListener("click", () => {
//   modal.style.display = "block";
//   document.body.style.overflow = "hidden"; // 스크롤바 제거
// });

// openModalCard.addEventListener("click", () => {
//   modal.style.display = "block";
//   document.body.style.overflow = "hidden"; // 스크롤바 제거
// });

// // 모달창 닫기
// closeModalBtn.addEventListener("click", () => {
//   modal.style.display = "none";
//   document.body.style.overflow = "auto"; // 스크롤바 보이기
// });

//지영 추가한 부분
$(document).on("click", ".ordernumber-btn", function () {
  // on 이벤트로 변경
  console.log("하이요");
  modal.style.display = "block";
  document.body.style.overflow = "hidden";
});


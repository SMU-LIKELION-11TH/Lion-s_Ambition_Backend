function onsubmitEmail() {
  // Simulating email verification
  const emailInput = document.getElementById('email');
  const email = emailInput.value;

  if (email.trim() === '') {
    alert('이메일을 입력해주세요.');
    return;
  }

  // Simulating asynchronous email verification request
  setTimeout(() => {
    const randomNumber = Math.floor(Math.random() * 100000);
    const numberInput = document.getElementById('number');
    numberInput.value = randomNumber;
    numberInput.setAttribute('data-random-number', randomNumber); // Save the random number as a data attribute
    alert(`이메일 인증번호: ${randomNumber}`);
  }, 2000);
}

function onclickckEmail() {
  const numberInput = document.getElementById('number');
  const enteredNumber = numberInput.value;

  if (enteredNumber.trim() === '') {
    alert('이메일 인증번호를 입력해주세요.');
    return;
  }

  // Simulating email verification check
  const randomNumber = numberInput.getAttribute('data-random-number');
  if (enteredNumber === randomNumber) {
    alert('이메일 인증이 완료되었습니다.');
  } else {
    alert('이메일 인증번호가 일치하지 않습니다.');
  }
}

function onsubmitSignup() {
  // Get form values
  const nicknameInput = document.getElementById('nickname');
  const emailInput = document.getElementById('email');
  const passwordInput = document.getElementById('password');
  const confirmPasswordInput = document.getElementById('confirm-password');

  const nickname = nicknameInput.value;
  const email = emailInput.value;
  const password = passwordInput.value;
  const confirmPassword = confirmPasswordInput.value;

  // Perform validation (e.g., check if required fields are filled, password match, etc.)
  if (nickname.trim() === '' || email.trim() === '' || password.trim() === '' || confirmPassword.trim() === '') {
    alert('모든 필드를 입력해주세요.');
    return;
  }

  if (password !== confirmPassword) {
    alert('비밀번호가 일치하지 않습니다.');
    return;
  }

  // Registration successful, perform further actions (e.g., send data to server)
  alert('회원가입이 완료되었습니다.');
  // Redirect to login page
  window.location.href = 'login_view.html';
}

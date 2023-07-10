function onSubmitLogin() {
    // 로그인 정보 가져오기
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    
    // 로그인 처리 및 리다이렉트
    if (username === 'your_email@example.com' && password === 'your_password') {
        alert('로그인 성공!');
        location.href = 'manage_view.html'; // 로그인 성공 시 이동할 페이지
    } else {
        alert('로그인 실패. 올바른 이메일과 비밀번호를 입력하세요.');
    }
}

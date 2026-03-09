document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const username = formData.get('username');
        const password = formData.get('password');

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 存储用户信息到 localStorage
                localStorage.setItem('user', JSON.stringify(data.user));
                window.location.href = '/'; // 重定向到首页或其他页面
            }else if(data.status === 'newUser'){
                return;
            }else {
                alert(data.message); // 显示错误信息
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('登录失败，请稍后再试。');
        });
    });
});

function toggleForms() {
    window.location.href = registerUrl;
}
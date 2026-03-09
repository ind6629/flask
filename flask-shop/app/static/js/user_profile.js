document.getElementById('avatar').addEventListener('change', function(e) {
    const fileName = e.target.files[0] ? e.target.files[0].name : '未选择文件';
    document.getElementById('file-name').textContent = fileName;
});

function logout() {
    const userStr = localStorage.getItem('user');
    if (userStr) {
        const user = JSON.parse(userStr);
        user.id = -1; // 手动清理修改用户状态
        localStorage.setItem('user', JSON.stringify(user)); // 重新存储
    }
    console.log(localStorage);
    window.location.href = logoutUrl;
}

function returnHome(){
    window.location.href = '/';
}
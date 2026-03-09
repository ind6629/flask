document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.product-link');

    links.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault(); // 阻止默认的链接跳转行为

            // 从 localStorage 获取用户信息
            const user = JSON.parse(localStorage.getItem('user'));
            const userId = user ? user.id : null;

            // 获取产品信息
            const productId = link.getAttribute('data-id');
            const category = link.getAttribute('data-category');

            // 发送请求到后端
            fetch('/api/tracking', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    event_id: productId,
                    event_type: 'product_click',
                    user_id: userId,
                    category: category
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                window.location.href = link.href; // 在请求成功后跳转到目标页面
            })
            .catch((error) => {
                console.error('Error:', error);
                window.location.href = link.href; // 即使请求失败也跳转到目标页面
            });
        });
    });
});

// 在控制台中检查 localStorage
console.log(JSON.parse(localStorage.getItem('user')));
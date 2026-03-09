document.addEventListener('DOMContentLoaded', () => {
    const addToCartButton = document.querySelector('#submitBtn');

        addToCartButton.addEventListener('click', (event) => {
            // 从 localStorage 获取用户信息
            const user = JSON.parse(localStorage.getItem('user'));
            const userId = user ? user.id : null;
            const productId = addToCartButton.getAttribute('data-id');
            const category = addToCartButton.getAttribute('data-category');
            // 发送请求到后端
            //fetch('/api/action_tracking', {
            fetch('/api/tracking', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    event_type: 'add_to_cart',
                    user_id: userId,
                    event_id: productId,
                    category: category
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                // 提交表单
                //form.submit();
                alert('success')
            })
            .catch((error) => {
                console.error('Error:', error);
                // 提交表单
                //form.submit();
                alert(error)
            });
        });
});
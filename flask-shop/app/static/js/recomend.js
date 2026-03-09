document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.recomend').forEach(function(element) {
        element.onclick = function(event) {
            event.preventDefault(); // 阻止默认的链接跳转行为

            const category = this.getAttribute('data-category'); // 动态获取 category
            let product_id;

            if (category === '苹果') {
                product_id = 100;
            } else if (category === '桔子') {
                product_id = 101;
            } else if (category === '香蕉') {
                product_id = 102;
            } else {
                // 默认情况或其他处理
                product_id = null; // 或者你可以设置一个默认的 product_id
            }

            if (product_id !== null) {
                const data = {
                    category: category,
                    product_id: product_id
                };

                fetch(`http://127.0.0.1:5001/my_main/${product_id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            } else {
                //console.error('Unknown category:', category);
            }
        };
    });
});
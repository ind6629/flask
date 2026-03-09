document.addEventListener('DOMContentLoaded', function() {
    // 取消收藏功能
    document.querySelectorAll('.remove-collection-btn').forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.stopPropagation();
        const item = this.closest('.collection-item');
        const productId = item.dataset.productId;
        console.log(productId);
        if (confirm('确定要从收藏中移除该商品吗？')) {
            $.ajax({
                type: "POST",
                url: removeCollectionUrl,
                data: productId,
                contentType: "application/json",
                dataType: "json",
                success: function(response) {
                  if(response.success){
                    item.remove();
                    alert(response.message);
                  }else{
                    alert('异常！！！');
                  }
                }
              });
        }
      });
    });
    
    // 加入购物车功能
    document.querySelectorAll('.add-to-cart-btn').forEach(btn => {
      btn.addEventListener('click', function() {
        const item = this.closest('.collection-item');
        const productId = item.dataset.productId;
        
        fetch('/cart/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token() }}'
          },
          body: JSON.stringify({
            product_id: productId,
            quantity: 1
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            showToast('已添加到购物车');
            updateCartCount(data.cart_count);
          } else {
            //showToast(data.message || '添加失败', 'error');
            console.log('暂时无法使用')
          }
        })
        .catch(error => {
          console.error('Error:', error);
          console.log('暂时无法使用')
          //showToast('网络错误，请重试', 'error');
        });
      });
    });
    
    // 显示提示消息
    function showToast(message, type = 'success') {
      const toast = document.createElement('div');
      toast.className = `toast ${type}`;
      toast.textContent = message;
      document.body.appendChild(toast);
      
      setTimeout(() => {
        toast.classList.add('show');
        setTimeout(() => {
          toast.remove();
        }, 3000);
      }, 100);
    }
    
    // 更新购物车数量
    function updateCartCount(count) {
      const cartCountEl = document.querySelector('.cart-count');
      if (cartCountEl) {
        cartCountEl.textContent = count;
        cartCountEl.classList.add('updated');
        setTimeout(() => {
          cartCountEl.classList.remove('updated');
        }, 500);
      }
    }
  });

function enterCart(){
  window.location.href = collectUrl;
}
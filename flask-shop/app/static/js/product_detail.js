function changeImage(thumbnail, newSrc) {
    // 切换主图
    document.getElementById('mainImage').src = newSrc;
    
    // 更新缩略图选中状态
    document.querySelectorAll('.thumbnail').forEach(img => {
        img.classList.remove('active');
    });
    thumbnail.classList.add('active');
}

document.querySelector('.quantity-minus').addEventListener('click', () => {
    const input = document.querySelector('.add-to-cart-number');
    input.value--;
  });
  
document.querySelector('.quantity-plus').addEventListener('click', () => {
    const input = document.querySelector('.add-to-cart-number');
    input.value++;
  });

document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const quantity = urlParams.get('quantity');
    const message = document.getElementById('message');
    const submitBtn = document.getElementById('submitBtn');
  
    if (quantity) {
        message.textContent  = "此次加入购物车成功，请注意数量："+quantity+"件";
        submitBtn.style.backgroundColor = 'orange';
    }
  });

function returnHome(){
    window.location.href = '/';
}

function addOrder(){
  const product_id = document.querySelector(".product-description").dataset.product_id;
  const product_price = document.querySelector(".product-description").dataset.product_price;
  const quantity = document.querySelector('.add-to-cart-number').value;
  console.log(product_id,product_price,quantity);
  url = orderUrl+"?product_id="+product_id+"&product_price="+product_price+"&quantity="+quantity;
  window.location.href = url;
}

document.getElementById('addOrder').addEventListener('click', () => {
  addOrder();
});

// const collectBtn = document.querySelector('#collect-btn')
// collectBtn.addEventListener('click', () => {
//   product_id = collectBtn.data_product_id;
//   user_id = collectBtn.user_id;
//    window.location.href = "{{ url_for('main.collect', product_id="+product_id+",user_id="+user_id+") }}"
// });

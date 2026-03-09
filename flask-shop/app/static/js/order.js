document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const selectAllCheckbox = document.getElementById('select-all');
    const footerSelectAll = document.getElementById('footer-select-all');
    const checkboxes = document.querySelectorAll('.order-checkbox:not(#select-all):not(#footer-select-all)');
    const deleteSelectedBtn = document.querySelector('.delete-selected');
    const selectedCountEl = document.querySelector('.selected-count');
    const totalPriceEl = document.querySelector('.total-price');
    const checkoutBtn = document.querySelector('.checkout-btn');
    
    // 更新选中状态和总价
    function updateSelection() {
      const selectedItems = document.querySelectorAll('.order-checkbox:checked:not(#select-all):not(#footer-select-all)');
      selectedCountEl.textContent = selectedItems.length;
      
      // 计算总价
      let total = 0;
      selectedItems.forEach(checkbox => {
        const priceEl = checkbox.closest('.order-item').querySelector('.item-price');
        const price = parseFloat(priceEl.textContent.replace(/[^0-9.]/g, ''));
        total += price;
      });
      
      totalPriceEl.textContent = `¥${total.toLocaleString('zh-CN', {minimumFractionDigits: 2})}`;
      
      // 更新全选状态
      const allChecked = selectedItems.length === checkboxes.length;
      selectAllCheckbox.checked = allChecked;
      footerSelectAll.checked = allChecked;
    }
    
    // 全选/取消全选
    function toggleSelectAll(checkbox) {
      const isChecked = checkbox.checked;
      checkboxes.forEach(cb => {
        cb.checked = isChecked;
      });
      updateSelection();
    }
    
    // 事件监听
    selectAllCheckbox.addEventListener('change', function() {
      toggleSelectAll(this);
    });
    
    footerSelectAll.addEventListener('change', function() {
      toggleSelectAll(this);
    });
    
    checkboxes.forEach(checkbox => {
      checkbox.addEventListener('change', updateSelection);
    });
    
    // 删除选中项
    deleteSelectedBtn.addEventListener('click', function() {
      const selectedItems = document.querySelectorAll('.order-checkbox:checked:not(#select-all):not(#footer-select-all)');
      if (selectedItems.length === 0) {
        alert('请先选择要删除的订单');
        return;
      }
      
      if (confirm(`确定要删除选中的 ${selectedItems.length} 个订单吗？`)) {
        order_ids = [];
        selectedItems.forEach(checkbox => {
          deleteItem = checkbox.closest('.order-item');
          order_ids.push(deleteItem.dataset.order_id);
          deleteItem.remove();
        });
        $.ajax({
          type: "POST",
          url: cancelOrderUrl,
          data: JSON.stringify(order_ids),
          contentType: "application/json",
          dataType: "json",
          success: function(response) {
            if(response.success){
              alert(response.message);
            }else{
              alert('异常！！！');
            }
          }
        });
      }
      updateSelection();
    });
    
    // 结算按钮
    checkoutBtn.addEventListener('click', function() {
      const selectedItems = document.querySelectorAll('.order-checkbox:checked:not(#select-all):not(#footer-select-all)');
      if (selectedItems.length === 0) {
        alert('请先选择要结算的订单');
        return;
      }
      order_ids = [];
      selectedItems.forEach(checkbox => {
        deleteItem = checkbox.closest('.order-item');
        order_ids.push(deleteItem.dataset.order_id);
        deleteItem.remove();
      });
      $.ajax({
        type: "POST",
        url: settleOrderUrl,
        data: JSON.stringify(order_ids),
        contentType: "application/json",
        dataType: "json",
        success: function(response) {
          if(response.success){
            alert(response.message);
          }else{
            alert('异常！！！');
          }
        }
      });
      
      alert(`正在结算 ${selectedItems.length} 个订单，总金额：${totalPriceEl.textContent}`);
    });
    
    // 初始化
    updateSelection();
  });
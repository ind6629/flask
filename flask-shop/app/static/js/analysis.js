document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    
    tabBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        // 移除所有active类
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        //document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
        
        // 添加active类到当前标签
        this.classList.add('active');
        //const tabId = this.getAttribute('data-tab');
        //document.getElementById(tabId).classList.add('active');
        const htmlSrc = this.getAttribute('data-htmlSrc');
        const iframe = document.createElement('iframe');
        iframe.src = htmlSrc;
        iframe.width = '100%';
        iframe.height = '500px';
        iframe.frameBorder = '0';
        iframe.allowFullscreen = true;
        contentBox = document.querySelector('.contentBox');
        //加载图标之前清除旧图表
        while (contentBox.firstChild) {
          contentBox.removeChild(contentBox.firstChild);
        }
        contentBox.appendChild(iframe);
      });
    });
    initClickTable();
});

function initClickTable(){
  defBtn = document.querySelector('#defaultBtn');
  defBtn.click();
}
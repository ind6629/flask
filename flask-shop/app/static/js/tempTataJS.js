document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.carousel-container');
    const slides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const indicators = document.querySelectorAll('.indicator');
    
    let currentIndex = 1; // 从原始第一张开始
    const totalSlides = slides.length;
    const realSlidesCount = 4; // 实际图片数量
    prevBtn.style.display = 'none';
    nextBtn.style.display = 'none';
    
    // 更新轮播图位置和指示器状态
    function updateCarousel() {
        container.style.transform = `translateX(-${currentIndex * 100}%)`;
        
        // 更新指示器
        let realIndex = getRealIndex();
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === realIndex);
        });
    }
    
    // 获取实际索引（排除克隆的幻灯片）
    function getRealIndex() {
        if (currentIndex === 0) return realSlidesCount - 1;
        if (currentIndex === totalSlides - 1) return 0;
        return currentIndex - 1;
    }
    
    // 下一张（无缝循环）
    function nextSlide() {
        currentIndex++;
        container.style.transition = 'transform 0.5s ease';
        updateCarousel();
        
        // 如果到达克隆的最后一张，无动画跳转到真实的第一张
        if (currentIndex === totalSlides - 1) {
            setTimeout(() => {
                container.style.transition = 'none';
                currentIndex = 1;
                container.style.transform = `translateX(-${currentIndex * 100}%)`;
            }, 500);
        }
    }
    
    // 上一张（无缝循环）
    function prevSlide() {
        currentIndex--;
        container.style.transition = 'transform 0.5s ease';
        updateCarousel();
        
        // 如果到达克隆的第一张，无动画跳转到真实的最后一张
        if (currentIndex === 0) {
            setTimeout(() => {
                container.style.transition = 'none';
                currentIndex = realSlidesCount;
                container.style.transform = `translateX(-${currentIndex * 100}%)`;
            }, 500);
        }
    }
    
    // 按钮点击事件
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    
    // 指示器点击事件
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', () => {
            currentIndex = index + 1;
            container.style.transition = 'transform 0.5s ease';
            updateCarousel();
        });
    });
    
    // 自动轮播
    let autoPlay = setInterval(nextSlide, 3000);
    
    // 鼠标悬停时暂停自动轮播
    document.querySelector('.carousel').addEventListener('mouseenter', () => {
        clearInterval(autoPlay);
        prevBtn.style.display = 'block';
        nextBtn.style.display = 'block';
    });
    
    // 鼠标离开时恢复自动轮播
    document.querySelector('.carousel').addEventListener('mouseleave', () => {
        autoPlay = setInterval(nextSlide, 3000);
        prevBtn.style.display = 'none';
        nextBtn.style.display = 'none';
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    
    tabBtns.forEach(btn => {
      btn.addEventListener('click', function() {
        // 移除所有active类
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-pane').forEach(pane => pane.classList.remove('active'));
        
        // 添加active类到当前标签
        this.classList.add('active');
        const tabId = this.getAttribute('data-tab');
        document.getElementById(tabId).classList.add('active');
      });
    });
  });
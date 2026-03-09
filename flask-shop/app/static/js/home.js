function user_profile() {
    window.location.href = userProfileUrl;
}

function login() {
    window.location.href = loginUrl;
}

function category(fixed_value) {
    window.location.href = `/category?fixed_value=${fixed_value}`;
}

function recomend(){
    window.location.href = recomendUrl;
}

function checkout(){
    window.location.href = checkoutUrl;
}

function help(){
    window.location.href = helpUrl;
}

function order(){
    window.location.href = orderUrl;
}

function refresh(){
    window.location.href = '/';
}

function collection(){
    window.location.href = collectUrl;
}

function analysis(){
    window.location.href = analysisUrl;
}

function search(){
    const keyword = document.querySelector('.search-input').value;
    console.log(keyword);

    // 从 localStorage 获取用户信息
    const user = JSON.parse(localStorage.getItem('user'));
    const userId = user ? user.id : '-1';

    const searchURL = '/result?'+'keyword='+keyword+'&'+'user_id='+userId;
    window.location.href = searchURL;

    // 发送请求到后端
    // fetch('/result', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json'
    //     },
    //     body: JSON.stringify({
    //         keyword: keyword,
    //         user_id: userId
    //     })
    // })
    // .then(response => response.json())
    // .then(data => {
    //     console.log('Success:', data);
    //     window.location.href = link.href; // 在请求成功后跳转到目标页面
    // })
    // .catch((error) => {
    //     console.error('Error:', error);
    //     window.location.href = link.href; // 即使请求失败也跳转到目标页面
    // });
}

document.addEventListener('DOMContentLoaded', function() {
    const categoryButtons = document.querySelectorAll('.category-button');

    categoryButtons.forEach(button => {
        button.addEventListener('mouseover', function() {
            const categories = JSON.parse(button.getAttribute('data-categories'));
            const detailsDiv = document.createElement('div');
            detailsDiv.className = 'category-details';

            categories.forEach(category => {
                const link = document.createElement('a');
                link.href = '#'; // 你可以根据需要修改链接
                link.textContent = category;
                detailsDiv.appendChild(link);
            });

            button.appendChild(detailsDiv);
        });

        button.addEventListener('mouseout', function() {
            const detailsDiv = button.querySelector('.category-details');
            if (detailsDiv) {
                detailsDiv.remove();
            }
        });
    });
});

//
likeBtn = document.querySelector('#like');
likeBtn.addEventListener('click', (e) => {
    //console.log('点击')

    const user = JSON.parse(localStorage.getItem('user'));
    const userId = user ? user.id : null;
    console.log('userId:',userId);
    if(userId==null){
        console.log('用户未登录!')
        return;    //登录后才可使用
    } 

    fetch('/api/trackResult', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user_id: userId
        })
    }).then(response => response.json())
        .then(data => {
            console.log('Success',data);
                const recommend_tab = document.getElementById('tab5');
                
                // 清空容器
                recommend_tab.innerHTML = '';
                
                // 动态生成商品卡片
                data.data.forEach(product => {
                  const card = `
                    <div class="product-item">
                        <a href="/product/${product.id}" class="product-link recomend" data-id="${ product.id }" data-category="${ product.category }">
                            <img src="${ product.image }" alt="${ product.name }" class="product-image">
                            <h3>"${ product.name }"</h3>
                            <p class="price">$${ product.price }</p>
                            <p class="stock">库存: ${ product.stock }</p>
                        </a>
                    </div>
                  `;
                  recommend_tab.insertAdjacentHTML('beforeend', card);
                });
        })
    })


// home.js
let slideIndex = 0;

// 轮播图图片数组
const carouselImages = [
    "/static/images/shuiguo.png",
    "/static/images/shucai.png",
    "/static/images/zhongyao.png",
    "/static/images/zhongmiao.png"
];

function showSlides() {
    const slides = document.querySelectorAll('.slides img');
    for (let i = 0; i < slides.length; i++) {
        slides[i].style.display = 'none';
    }
    slideIndex++;
    if (slideIndex > slides.length) { slideIndex = 1 }
    slides[slideIndex - 1].style.display = 'block';
    setTimeout(showSlides, 3000); // 每3秒切换一次图片
}

function plusSlides(n) {
    showSlides(slideIndex += n);
}

// 动态生成轮播图图片
function generateCarouselImages() {
    const slidesContainer = document.getElementById('carousel-slides');
    carouselImages.forEach(imageSrc => {
        const imgElement = document.createElement('img');
        imgElement.src = imageSrc;
        imgElement.style.display = 'none';
        slidesContainer.appendChild(imgElement);
    });
    showSlides(); // 初始化显示第一张图片
}

// 页面加载时生成轮播图
document.addEventListener('DOMContentLoaded', generateCarouselImages);


document.addEventListener('DOMContentLoaded', function () {
    // 数据集
    var data1 = {
        labels: ['6月', '7月', '8月', '9月', '10月', '11月'],
        datasets: [{
            label: '苹果价格趋势',
            data: [12, 19, 3, 5, 2, 3],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: false
        }]
    };

    var data2 = {
        labels: ['6月', '7月', '8月', '9月', '10月', '11月'],
        datasets: [{
            label: '大米价格趋势',
            data: [20, 15, 10, 18, 12, 14],
            borderColor: 'rgba(153, 102, 255, 1)',
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            fill: false
        }]
    };

    // 配置
    var options = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    };

    // 创建图表
    var ctx1 = document.getElementById('chart1').getContext('2d');
    var chart1 = new Chart(ctx1, {type: 'line', data: data1, options: options});

    var ctx2 = document.getElementById('chart2').getContext('2d');
    var chart2 = new Chart(ctx2, {type: 'line', data: data2, options: options});
});

const cartButton = document.getElementById('cartButton');
const modal = document.getElementById('cartModal');
const closeBtn = document.querySelector('.close');
const cancel = document.getElementById('cancel');
const helpBtn = document.getElementById('helpBtn');

// 打开弹窗（带动画）
cartButton.addEventListener('click', () => {
  modal.classList.add('active'); // 触发CSS动画
});

// 关闭弹窗（带动画）
closeBtn.addEventListener('click', () => {
  modal.classList.remove('active');
});
cancel.addEventListener('click', () => {
    modal.classList.remove('active');
});

// 点击遮罩层关闭
window.addEventListener('click', (e) => {
  if (e.target === modal) {
    modal.classList.remove('active');
  }
});



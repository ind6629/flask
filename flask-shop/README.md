代码在app目录下

models——模型文件（数据库操作）
    cart——购物车模型
    comment——评论模型
    news——新闻模型
    orders——订单模型
    product——商品模型
    track——埋点模型
    user——用户模型

routes——路由文件(功能)
    auth——认证文件（登录/注册、注销）
    buy——购物车相关（添加到购物车、删除购物车）
    comments——评论相关（添加评论）  
    main——商品相关（商品列表、商品的增删改查等、获取新闻列表）
    track——埋点相关（埋点）


static——静态文件
    css——css文件
    js——js文件
        cart_tracking.js——添加购物车埋点js文件
        home.js——首页js文件(轮播图等)
        login.js——登录模板js文件
        tracking.js——埋点js文件(收集用户点击的商品分类,商品id,用户id)
    images——图片文件

templates——模板文件（前端页面）
    about.html——关于模板
    add_product.html——添加商品模板
    cart.html——购物车模板
    content.html——资讯模板
    edit_product.html——编辑商品模板
    help.html——帮助模板
    home.html——首页模板
    login.html——登录模板
    nongxiaoling.html——大模型模板
    product_detail.html——商品详情模板
    register.html——注册模板
    user_profile.html——个人中心模板

__init__.py —— 初始化文件(蓝图)
db.py —— 数据库文件
from django.conf.urls import url
from app import views


appname = 'app'
urlpatterns = [
    # 主页
    url(r'^home/', views.home),
    # 登录注册和退出
    url(r'^regist/', views.regist),
    url(r'^login/', views.login),
    url(r'^logout', views.logout),

    # 自己写的闪购页面
    # url(r'^market/', views.market),

    # 新的闪购页面的url
    url(r'^newmarket/$', views.user_market, name='market'),
    url(r'^newmarket/(\d+)/(\d+)/(\d+)/', views.user_market_params, name='marketparams'),

    # 自己的主页面
    url(r'^mine/', views.mine),

    # 添加和删除购物车数据
    url(r'^maddgoods/', views.add_goods, name='maddgoods'),
    url(r'^msubgoods/', views.sub_goods, name='msubgoods'),

    # 购物车页面
    url(r'^cart/', views.cart),

    # 改变选择页面
    url(r'^change_choose/', views.change_choose, name='change_c'),

    # 购物车全选url
    url(r'^select_all/', views.select_all, name='select_all'),


    # 订单页面
    url(r'^deal_table_number/', views.deal_table_number, name='d_t_n'),
    url(r'^order_info/(\d+)/', views.order_info, name='order_info'),

    # 取消订单
    url(r'^delete_order/', views.delete_good),

    # 待付款页面
    url(r'^wait_pay/', views.wait_pay),

    # 待收货页面
    url(r'^wait_recieve/', views.wait_recieve)


]
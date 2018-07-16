
from datetime import datetime
import random, time

from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from django.core.urlresolvers import reverse
from app.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, UserModel, OrderModel, FoodType, Goods, \
    CartModel, OrderGoodsModel
from utils.functions import get_ticket


def home(request):
    """
    把数据库数据解析到首页界面
    :param request: '/xrf/home/'首页的请求url
    :return: 首页的界面
    """
    wheels = MainWheel.objects.all()
    navs = MainNav.objects.all()
    mustbuys = MainMustBuy.objects.all()
    shops = MainShop.objects.all()
    shop0 = shops[0]
    shop12 = shops[1:3]
    shop3456 = shops[3:7]
    shop78910 = shops[7:]
    shows = MainShow.objects.all()
    data = {
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shop0': shop0,
        'shop12': shop12,
        'shop3456': shop3456,
        'shop78910': shop78910,
        'shows': shows,
    }

    return render(request, 'home/home.html', data)


def regist(request):
    """
    通过页面的表单的post请求把注册信息写到数据库中
    :param request: '/axf/regist/'用户注册的请求url
    :return: 注册完成返回到登录界面
    """
    if request.method == 'GET':
        return render(request, 'user/user_register.html')

    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        img = request.FILES.get('icon')

        password = make_password(password)

        UserModel.objects.create(
            username=name,
            password=password,
            email=email,
            icon=img,
        )
        return HttpResponseRedirect('/axf/login/')


def login(request):
    """

    :param request: '/axf/login/'登录界面的请求url
    :return: 登录成功返回到首页;登录不成功:1)用户不存在返回注册界面 2)用户存在
    """
    if request.method == 'GET':
        return render(request, 'user/user_login.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=username).exists():
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                ticket = get_ticket()
                response = HttpResponseRedirect('/axf/home/')
                response.set_cookie('ticket', ticket, max_age=432000)
                user.ticket = ticket
                user.save()
                return response
            else:
                return render(request, 'user/user_login.html', {'password': '密码错误'})
        else:
            return render(request, 'user/user_login.html', {'username': '用户名错误'})


def logout(request):

    if request.method == 'GET':
        response = HttpResponseRedirect('/axf/mine/')
        response.delete_cookie('ticket')
        return response


def mine(request):
    """
    我的主页
    :param request: '/axf/mine/'我的主页的请求的url
    :return: 返回我的主页
    """
    if request.method == 'GET':
        user = request.user
        order_id = request.GET.get('order_id_payed')
        if user and user.id:
            wait_pay, wait_recieve = 0, 0
            orders = OrderModel.objects.all()
            order = OrderModel.objects.filter(id=order_id).first()
            if order_id:
                order.o_status = 1
                order.save()
            for order in orders:
                if order.o_status == 0:
                    wait_pay += 1
                elif order.o_status == 1:
                    wait_recieve += 1
                elif order.o_status == 2:
                    wait_recieve += 1
            data = {
                'wait_pay': wait_pay,
                'wait_recieve': wait_recieve,
            }
            return render(request, 'mine/mine.html', data)
        else:
            return HttpResponseRedirect('/axf/login/')

# 下面是自己写的闪购页面
# def market(request):
#     """
#     闪购界面
#     :param request: '/axf/market/'闪购界面的请求url
#     :return: 返回闪购界面
#     """
#     if request.method == 'GET':
#         foodtypes = FoodType.objects.all()
#         # goods = Goods.objects.all()
#         s = request.GET
#         typeid = s.get('typeid')
#         childcidname = s.get('childcidname')
#
#         if not typeid:
#             goods = Goods.objects.filter(childcidname=childcidname)
#             if not childcidname:
#                 goods = Goods.objects.all()
#         else:
#             goods = Goods.objects.filter(categoryid=typeid)
#
#         good_type = goods.values('childcidname').distinct()
#
#         data = {
#             'foodtypes': foodtypes,
#             'goods': goods,
#             'good_type': good_type,
#         }
#         return render(request, 'market/market.html', data)


def user_market(request):
    """
    默认中间跳转参数传递
    :param request:'/axf/newmarket/'中间默认参数传递的url
    :return:跳转到视图views.user_market_params
    """
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('axf:marketparams', args=('103532', '0', '0')))


def user_market_params(request, typeid, childid, sort_id):
    """
    闪购页面
    :param request:‘/axf/newmarket/103532/0/0/’默认的闪购页面请求的url
    :param typeid:食品分类的id
    :param childid:具体某一类下的再分类的id
    :param sort_id:排序id
    :return:返回闪购页面
    """

    if request.method == 'GET':

        # 获取所有的商品类型
        foodtypes = FoodType.objects.all()
        # 获取某一商品类型下的所有食物类型
        goods_type = Goods.objects.filter(categoryid=typeid)

        # 如果选择某一商品类型下的食物类型
        if childid != '0':
            # 是否按某种方式排序
            if sort_id == '0':
                goods_type = Goods.objects.filter(categoryid=typeid,
                                                  childcid=childid)
            elif sort_id == '1':
                goods_type = Goods.objects.filter(categoryid=typeid,
                                                  childcid=childid).order_by('productnum')
            elif sort_id == '2':
                goods_type = Goods.objects.filter(categoryid=typeid,
                                                  childcid=childid).order_by('-price')

            elif sort_id == '3':
                goods_type = Goods.objects.filter(categoryid=typeid,
                                                  childcid=childid).order_by('price')
            else:
                goods_type = Goods.objects.filter(categoryid=typeid,
                                                  childcid=childid)
        # 如果只选择商品类型
        else:
            # 是否按某种方式排序
            if sort_id == '0':
                pass
            elif sort_id == '1':
                goods_type = Goods.objects.filter(categoryid=typeid).order_by('productnum')
            elif sort_id == '2':
                goods_type = Goods.objects.filter(categoryid=typeid).order_by('-price')

            elif sort_id == '3':
                goods_type = Goods.objects.filter(categoryid=typeid).order_by('price')

        childtypeobj = FoodType.objects.get(typeid=typeid)
        # 从数据库中获取具体的食物分类类型名
        childtypes = childtypeobj.childtypenames.split('#')
        childtype = []
        for t in childtypes:
            childtype.append(t.split(':'))

        data = {
            'foodtypes': foodtypes,
            'goods_type': goods_type,
            'childtypes': childtype,
            'typeid': typeid,
            'childid': childid,
            'sort_id': sort_id,
        }

        return render(request, 'market/newmarket.html', data)

# 增加商品数量
# 1) 闪购页面数量增加
# 2) 购物车页面商品数量的增加
# 在购物车页面下，如果点击增加按钮：1)商品已经勾选，数量增加保存到数据库，总价增加，然后在页面显示
#2)商品未勾选，数量增加保存到数据库中，商品还要勾中，总价增加，然后渲染到页面上，还要判断勾选后是否所有商品都勾选如果勾选，则全选勾中


def add_goods(request):
    """增加商品数量"""

    if request.method == 'POST':
        user = request.user
        data = {
            'msg': '请求成功',
            'code': 200,
        }
        if user and user.id:
            goods_id = request.POST.get('goods_id')
            # 获取购物车对应商品的信息
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()

            # 如果购物车有了该商品
            if user_carts:
                user_carts.c_num += 1  # 商品数量加1
                user_carts.save()      # 保存到数据库中
                is_select = user_carts.is_select   # 拿到该商品是否被选中True or False
                data['c_num'] = user_carts.c_num   # 拿到该商品增加后的数量，最后返给页面
                if not is_select:                  # 如果商品没有被选中
                    data['is_select'] = is_select  # 把is_select返给ajax函数成功后中的msg
                    user_carts.is_select = 1       # 点击后就把该商品选中把数据库中的is_select值变成1
                    user_carts.save()              # 保存到数据库中
                    # 判断商品是否全部选中
                    carts = CartModel.objects.all()
                    is_select_all = True
                    for cart in carts:
                        if not cart.is_select:
                            is_select_all = False
                    data['is_select_all'] = is_select_all
            else:
                # 如果购物车没有该商品选商品
                CartModel.objects.create(user=user,
                                         goods_id=goods_id,
                                         c_num=1)
                data['c_num'] = 1
            data['total_price'] = total_price()

        return JsonResponse(data)


def sub_goods(request):
    """减少商品数量"""

    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {
            'msg':'请求成功',
            'code': 200,
        }
        if user and user.id:

            # 查看商品是否在购物车中
            user_carts = CartModel.objects.filter(user=user, goods_id=goods_id).first()
            # 如果存在，则减一
            if user_carts:
                is_select = user_carts.is_select
                if not is_select:
                    data['is_select'] = is_select
                    user_carts.is_select = 1
                    user_carts.save()

                # 如果商品的数量为1，则删除
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0

                    # 判断剩下的商品是否是全部选中
                    carts = CartModel.objects.all()
                    is_select_all = True
                    for cart in carts:
                        if not cart.is_select:
                            is_select_all = False
                    data['is_select_all'] = is_select_all

                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num

                    # 判断商品是否全部选中
                    carts = CartModel.objects.all()
                    is_select_all = True
                    for cart in carts:
                        if not cart.is_select:
                            is_select_all = False
                    data['is_select_all'] = is_select_all
                data['total_price'] = total_price()

        return JsonResponse(data)


def cart(request):
    """
    购物车界面
    :param request: '/axf/cart/'购物车界面的请求url
    :return: 返回购物车界面
    """
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            carts = CartModel.objects.filter(user_id=user.id)
            # 用来判断是否要在页面显示全选
            # 如果所有商品都选中的话，则打√，只要有一个商品没有选中，则打×
            is_select_all = True
            for cart in carts:
                if not cart.is_select:
                    is_select_all = False
            data = {
                'total_price': total_price(),
                'carts': carts,
                'is_select_all': is_select_all,
            }
            return render(request, 'cart/cart.html', data)
        else:
            HttpResponseRedirect('/axf/login/')


# 计算购物车选中商品的总价，用来被调用，很多地方都要进行商品总价的在计算
def total_price():
    """计算选中商品的总价"""
    carts = CartModel.objects.filter(is_select=True)
    total_price = 0
    for cart in carts:
        if cart.is_select:
            num = cart.c_num
            price = cart.goods.price
            total_price += num * price
    total_price = '%.1f' % total_price

    return total_price


def change_choose(request):
    """点击商品前的选中按钮函数"""

    if request.method == 'POST':
        user = request.user
        goods_id = request.POST.get('goods_id')
        data = {
            'msg': '请求成功',
            'code': 200
        }
        cartobj = CartModel.objects.filter(user=user, goods_id=goods_id).first()
        if cartobj.is_select:
            is_select = False
            cartobj.is_select = 0
        else:
            is_select = True
            cartobj.is_select = 1
        cartobj.save()

        # 用来判断是否商品全部选中
        carts = CartModel.objects.filter(user=user)
        is_select_all = True
        for cart in carts:
            if not cart.is_select:
                is_select_all = False
        data['is_select_all'] = is_select_all

        data['is_select'] = is_select
        data['total_price'] = total_price()
        return JsonResponse(data)


is_choose = True # 为全选按钮设置的全局变量


def select_all(request):
    """全选按钮函数"""

    if request.method == 'GET':
        global is_choose
        is_choose = not is_choose
        user = request.user
        carts = CartModel.objects.filter(user=user)
        if user and user.id:
            goods = []
            data = {}
            if not is_choose:
                for cart in carts:
                    cart.is_select = 0
                    cart.save()
                carts1 = CartModel.objects.all()
                for cart1 in carts1:
                    goods.append(cart1.goods_id)
                data['total_price'] = 0
            else:
                for cart in carts:
                    cart.is_select = 1
                    cart.save()
                carts2 = CartModel.objects.all()
                data['total_price'] = total_price()
                for cart2 in carts2:
                    goods.append(cart2.goods_id)
            data['goods'] = goods
            data['is_choose'] = is_choose

            return JsonResponse(data)


def deal_table_number(request):
    """点击下单对数据库中的表数据进行处理的函数"""
    # 点击下单后，要生成订单表和订单信息详情表，购物车表选中的数据要删除
    if request.method == 'GET':
        user = request.user
        carts = CartModel.objects.filter(user=user, is_select=True)
        if user and user.id:
            if len(carts) != 0:
                order = OrderModel.objects.create(user=user)

                for cart in carts:
                    OrderGoodsModel.objects.create(goods_num=cart.c_num,
                                                   goods_id=cart.goods_id,
                                                   order_id=order.id)
                carts.delete()
                order_id = str(order.id)
                return HttpResponseRedirect(reverse('axf:order_info', args=(order_id,)))
            else:
                return HttpResponseRedirect('/axf/cart/')


def order_info(request, order_id):
    """
    订单页面数据处理
    :param request:'/axf/cart/'订单页面的请求url
    :param order_id: 生成订单的订单号
    :return: 订单页面
    """
    if request.method == 'GET':
        user = request.user
        order_id = int(order_id)
        if user and user.id:

            order_goods = OrderGoodsModel.objects.filter(order_id=order_id)
            data = {
                'order_id': order_id,
                'order_goods': order_goods,
            }
            return render(request, 'order/order_info.html', data)
        else:
            return HttpResponseRedirect('/axf/login/')


def delete_good(request):
    """处理订单页面中是否要取消订单"""
    if request.method == 'GET':
        user = request.user
        order_id = request.GET.get('order_id')
        if user and user.id:
            if order_id:
                order_good = OrderGoodsModel.objects.filter(order_id=order_id)
                order = OrderModel.objects.filter(id=order_id)
                order.delete()
                order_good.delete()

                return HttpResponseRedirect('/axf/cart/')


def wait_pay(request):
    """待付款页面的业务逻辑处理"""
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.all()
            data = {
                'orders': orders,
            }
            return render(request, 'order/order_list_wait_pay.html', data)


def wait_recieve(request):
    """待收货的页面信息"""
    if request.method == 'GET':

        user = request.user
        if user and user.id:
            orders = OrderModel.objects.all()
            data = {
                'orders': orders,
            }
            return render(request, 'order/order_list_payed.html', data)







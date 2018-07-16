from django.db import models

# Create your models here.


class Main(models.Model):
    """
    图片数据父类，只能用来被继承
    img 分类图片
    name 用来描述图片的名字
    trackid 通用id
    """
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=16)

    class Meta:
        abstract = True # abstract摘要；抽象；


class MainWheel(Main):
    # 轮循banner
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    # 导航
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    # 必购
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    # 商店
    class Meta:
        db_table = 'axf_shop'


# 主要展示商品
class MainShow(Main):
    """
    img 商品图片
    longname 商品名称
    price 优惠价格
    marketprice 原始价格
    """
    categoryid = models.CharField(max_length=16, null=True)
    brandname = models.CharField(max_length=100, null=True)
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16, null=True)
    productid1 = models.CharField(max_length=16, null=True)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=1)
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16, null=True)
    productid2 = models.CharField(max_length=16, null=True)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16, null=True)
    productid3 = models.CharField(max_length=16, null=True)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):
    """
    闪购页面的食物分类模型
    typeid 食品分类的唯一id
    typename 食品分类名字
    """
    typeid = models.CharField(max_length=16)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    """
    productid 商品的id
    productimg 商品的图片
    productname 商品的名称
    productlongname 商品的规格
    isxf
    pmdesc
    specifics 详细规格
    price 折后价格
    marketprice 原价
    categoryid 当前分类id
    childid 子分类id
    childidname 子分类id 名字
    dealerid
    storenums 排序
    productnum 销售排序

    """
    productid = models.CharField(max_length=16)
    productimg = models.CharField(max_length=200)
    productname = models.CharField(max_length=100)
    productlongname = models.CharField(max_length=200)
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.CharField(max_length=16)
    childcid = models.CharField(max_length=16)
    childcidname = models.CharField(max_length=100)
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_goods'


class UserModel(models.Model):
    """
    username 用户名
    password 用户密码
    email 用户密码
    sex 性别
    icon 用户头像
    is_delete 是否删除
    """
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icons')
    is_delete = models.BooleanField(default=False)
    ticket = models.CharField(max_length=128, null=True)

    class Meta:
        db_table = 'axf_users'


# 购物车
class CartModel(models.Model):
    """
    购物车表
    user 表示关联用户
    goods 表示关联商品
    c_num 表示商品个数
    is_select 是否选中商品
    """
    user = models.ForeignKey(UserModel)
    goods = models.ForeignKey(Goods)
    c_num = models.IntegerField(default=1)
    is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'


class OrderModel(models.Model):
    """
    订单表
    user 关联用户
    o_num 数量
    o_status
    0 代表已下单，但是未付款， 1 已付款未发货， 2 已付款，已发货......
    o_create 创建时间
    """
    user = models.ForeignKey(UserModel)
    o_num = models.CharField(max_length=64)
    o_status = models.IntegerField(default=0)
    o_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    """
    商品订单详细信息表
    goods 关联商品表
    order 关联订单表
    goods_num 商品的个数
    """
    goods = models.ForeignKey(Goods)
    order = models.ForeignKey(OrderModel)
    goods_num = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_order_goods'

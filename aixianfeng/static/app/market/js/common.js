
// 点击增加(+)按钮
// 1)在闪购页面添加商品，商品的数量增加($('#num_' + goods_id).html(msg.c_num);)
// 2)在购物车页面点击添加(+)按钮:1)商品数量增加.2)如果商品没有选中，点击添加商品就要选中.
// 3)拿到计算选中的总价并渲染到页面( $('#total_price').html('总价:' + msg.total_price);)
function addShop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var url = '/axf/maddgoods/';
    $.ajax({
        url: url,
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg){
            console.log(msg);
            $('#num_' + goods_id).html(msg.c_num);
            $('#total_price').html('总价:' + msg.total_price);
            // 如果该商品没有选中，点击后选中
            if(!msg.is_select){
                $('#changeselect_' + goods_id).html(
                    '<span onclick="change_choose('+ goods_id +')">' + '√' + '</span>'
                )
            }
            // 如果所有商品都选中的话，全选选中
            if(msg.is_select_all){
                $('#is_select_all').each(function () {
                    $(this).replaceWith('<span id="is_select_all" onclick="select_all()">' + '√' + '</span>')
                })
            }

        },
        error:function(msg) {
            alert('请求错误')
        }

    })
}


// 点击减少(-)按钮
function subShop(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var url = '/axf/msubgoods/';
    $.ajax({
        url: url,
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            $('#num_' + goods_id).html(msg.c_num);
            $('#total_price').html('总价:'+ msg.total_price);
            // 如果该商品没有选中的话，点击后选中
            if(!msg.is_select){
                $('#changeselect_' + goods_id).html(
                    '<span onclick="change_choose('+ goods_id +')">' + '√' + '</span>'
                )
            }
            // 如果剩下的商品全部选中则全选选中
            if(msg.is_select_all){
                $('#is_select_all').each(function () {
                    $(this).replaceWith('<span id="is_select_all" onclick="select_all()">' + '√' + '</span>')
                })
            }

        },
        error:function (msg) {
            alert('请求错误')
        }

    })
}

// 点击某一商品勾选(√)按钮
//此函数改变购物车具体的商品是否选中
// 1)如果所有的商品都选中，全选按钮选中，总价要渲染
// 2)如果有其中一个没有选中，全选就没有选中，总价要渲染
function change_choose(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var url = '/axf/change_choose/';
    $.ajax({
        url: url,
        type: 'POST',
        data: {'goods_id': goods_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success:function (msg) {
            console.log(msg);
            $('#total_price').html('总价:' + msg.total_price);
            // msg.is_select=true,表示商品选中，商品就应该打'√'，否则打'×'

            if (msg.is_select){
               $('#changeselect_' + goods_id).html(
                   '<span onclick="change_choose('+ goods_id +')">' + '√' + '</span>'
               )
            }else{
                $('#changeselect_' + goods_id).html(
                    '<span onclick="change_choose('+ goods_id +')">' + '×' + '</span>'
                )
            }
            // msg.is_select_all=true, 表示所有商品都选中全选打√，否则全选打×
            if(msg.is_select_all){
                $('#is_select_all').each(function () {
                    $(this).replaceWith('<span id="is_select_all" onclick="select_all()">' + '√' + '</span>')
                })
            }else{
                $('#is_select_all').each(function () {
                    $(this).replaceWith('<span id="is_select_all" onclick="select_all()">' + '×' + '</span>')
                })

            }
        },
        error:function (msg) {
            alert('请求失败')
        }
    })
}


// 点击全选按钮
function select_all() {
   var url = '/axf/select_all/';
   $.ajax({
       url: url,
       type: 'GET',
       dataType: 'json',
       success:function (msg) {
           console.log(msg);
           $('#total_price').html('总价:'+ msg.total_price);
           var goods_id = msg.goods;
           if(msg.is_choose){
               $('#is_select_all').each(function () {
                   $(this).replaceWith('<span id="is_select_all" onclick="select_all()">' + '√' + '</span>')
                });

               for (var i = 0; i < goods_id.length; i++){
                   var good_id = goods_id[i];
                   $('#changeselect_' + good_id).html(
                       '<span onclick="change_choose('+ good_id +')">' + '√' + '</span>'
                   )
               }
            }else{
               $('#is_select_all').each(function () {
                   $(this).replaceWith('<span id="is_select_all" onclick="select_all()">' + '×' + '</span>')
                });
               for (var i = 0; i < goods_id.length; i++){
                   var good_id = goods_id[i];
                   $('#changeselect_' + good_id).html(
                       '<span onclick="change_choose('+ good_id +')">' + '×' + '</span>'
                   )
               }
            }
        },
        error:function () {
           alert('请求失败')
        }
    });
}






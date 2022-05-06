// 显示当前账单
function showCustomerOrder(order_id, food, total_price, merchant_take_order, rider) {
    $('.current-order tbody').append(`<tr>
                                         <td>${order_id}</td>
                                         <td>${food}</td>
                                         <td>${total_price}￥</td>
                                         <td>${merchant_take_order}</td>
                                         <td>${rider}</td>
                                         <td><a href="/chat/?orderid=${order_id}"><i class="material-icons">call</i></a></td>
                                     </tr>`)
}

// 显示可接账单
function merchantTakeOrderList(food, total_price, order_id) {
    $('.take-order tbody').append(`<tr>
                                       <td>${food}</td>
                                       <td>${total_price}￥</td>
                                       <td><input type="text" class="rider-salary" value="0">￥</td>
                                       <td><i class="material-icons m-take-order" order_id="${order_id}">done</i></td>
                                   </tr>`)
}

// 接单符号的点击事件
function merchantTakeOrder() {
    $('.m-take-order').on('click', function (e) {
        let order_id = $(e.target).attr('order_id');
        let rider_salary = $(e.target).parent().prev().children().val()
        $.ajax({
            type: 'PUT',
            url: '/elebu/api/v1/order/',
            data: {
                order_id: order_id,
                rider_salary: rider_salary
            },
            success: function (resp) {
                if (resp['status'] === 200) {
                    $(e.target).parent().parent().remove();
                    Materialize.toast('接单成功', 4000);
                } else {
                    Materialize.toast('接单失败', 4000);
                }
            },
            error: function () {
                Materialize.toast('接单失败', 4000);
            }
        });
    });
}

// 骑手可接订单
function riderTakeOrderList(order_id, food, salary) {
    $('.take-order tbody').append(`<tr>
                                       <td>${order_id}</td>
                                       <td>${food}￥</td>
                                       <td>${salary}￥</td>
                                       <td><i class="material-icons r-take-order" order_id="${order_id}">done</i></td>
                                   </tr>`)
}

// 骑手接单
function riderTakeOrder() {
    $('.r-take-order').on('click', function (e) {
        let order_id = $(e.target).attr('order_id');
        $.ajax({
            type: 'PUT',
            url: '/elebu/api/v1/order/',
            data: {
                order_id: order_id
            },
            success: function (resp) {
                if (resp['status'] === 200) {
                    $(e.target).parent().parent().remove();
                    Materialize.toast('接单成功', 4000);
                } else {
                    Materialize.toast('接单失败', 4000);
                }
            },
            error: function () {
                Materialize.toast('接单失败', 4000);
            }
        });
    });
}

// 送达
function riderCheckTable() {
    $('#test2').append(`<div class="col s12">
                                        <table class="striped responsive-table check-arrive">
                                            <thead>
                                            <tr>
                                                <th data-field="food_name">菜品</th>
                                                <th data-field="order_id">订单号</th>
                                                <th data-field="rider-salary">骑手收入</th>
                                                <th data-field="arrive">送达</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            </tbody>
                                        </table>
                                    </div>`)
}

function riderCheckArriveList(order_id, food, rider_salary) {
    $('.check-arrive tbody').append(`<tr>
                                       <td>${order_id}</td>
                                       <td>${food}￥</td>
                                       <td>${rider_salary}￥</td>
                                       <td><i class="material-icons r-check" order_id="${order_id}">done</i></td>
                                   </tr>`);

}

// 确认送达
function riderCheckArrive() {
    $('.r-check').click(function (e) {
        console.log($(e.target).attr('order_id'));
        $.ajax({
            type: 'PUT',
            url: '/elebu/api/v1/order/',
            data: {
                arrive: 'arrive',
                order_id: $(e.target).attr('order_id')
            },
            success: function (resp) {
                if (resp['status'] === 200) {
                    $(e.target).parent().parent().remove();
                    Materialize.toast('送达', 4000);
                } else {
                    Materialize.toast('请再次确认', 4000);
                }
            },
            error: function () {
                Materialize.toast('请再次确认', 4000);
            }
        });
    });
}

// 获取订单，并展示
function showOrders(user_id, role) {
    let r = typeof role !== 'undefined' ? role : 'customer';
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/order/',
        data: {
            user_id: user_id,
            role: r
        },
        success: function (resp) {
            if (r === 'merchant') {
                $('ul.tabs').append(`<li class="tab col"><a class="teal-text" href="#test5">商家接单</a></li>`);
                $(`<div id="test5" class="col s12"></div>`).appendTo('.container');
                $('#test5').append(`<div class="col s12">
                                        <table class="striped responsive-table take-order">
                                            <thead>
                                            <tr>
                                                <th data-field="food_name">菜品</th>
                                                <th data-field="total_price">用户支付</th>
                                                <th data-field="rider-salary">骑手收入</th>
                                                <th data-field="take-order">接单</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            </tbody>
                                        </table>
                                    </div>`)
            } else if (r === 'rider') {
                riderCheckTable();
                $('ul.tabs').append(`<li class="tab col"><a class="teal-text" href="#test5">骑手接单</a></li>`);
                $(`<div id="test5" class="col s12"></div>`).appendTo('.container');
                $('#test5').append(`<div class="col s12">
                                        <table class="striped responsive-table take-order">
                                            <thead>
                                            <tr>
                                                <th data-field="order_id">订单号</th>
                                                <th data-field="food_name">菜品</th>
                                                <th data-field="rider-salary">骑手收入</th>
                                                <th data-field="take-order">接单</th>
                                            </tr>
                                            </thead>
                                            <tbody>
                                            </tbody>
                                        </table>
                                    </div>`)
            }
            if (resp['status'] === 200) {
                for (let info of resp['info']) {
                    // 是否送达
                    let arrive = '';
                    if (info['arrive']) {
                        arrive = info['arrive'];
                    }
                    let customer_id = info['customer_id'];
                    // 商家id
                    let merchant_id = info['merchant_id'];
                    // 食物
                    let food = info['food'];
                    // 商家接单
                    let merchant_take_order = '';
                    if (info['merchant_take_order']) {
                        merchant_take_order = '<i class="material-icons">done</i>';
                    }
                    // 骑手接单
                    let rider_salary = info['rider_salary'];
                    let rider_id = info['rider_id'];
                    let rider = '';
                    if (info['rider_id']) {
                        rider = `${info['rider_id']}号骑手为您送餐`
                    }
                    // 订单号
                    let order_id = info['order_id'];
                    // 总价
                    let total_price = info['total_price'];
                    // 赞
                    let zan = info['zan'];
                    // dom
                    if (r === 'customer') {
                        if (!arrive) {
                            showCustomerOrder(order_id, food, total_price, merchant_take_order, rider);
                        }
                    } else if (r === 'merchant') {
                        merchantTakeOrderList(food, total_price, order_id);
                    } else if (r === 'rider') {
                        if (!rider_salary) {
                            rider_salary = 0;
                        }
                        if (!rider_id && info['merchant_take_order']) {
                            riderTakeOrderList(order_id, food, rider_salary);
                        } else if (rider_id && !arrive) {
                            riderCheckArriveList(order_id, food, rider_salary);
                        }
                    }
                }
            }
            merchantTakeOrder();
            riderTakeOrder();
            riderCheckArrive();
        },
        error: function () {

        }
    });
}

// 获取标签
function getTags() {
    $.ajax({
        method: 'GET',
        url: '/elebu/api/v1/tag/',
        success: function (resp) {
            let d = resp['data'];
            $('.chips-initial').material_chip({
                placeholder: '添加标签',
                data: d
            });
        },
        error: function () {
            Materialize.toast('获取标签失败，请刷新页面', 4000);
        }
    });
}

// 添加标签
function addTags(e, chip) {
    $.ajax({
        type: 'POST',
        url: '/elebu/api/v1/tag/',
        data: {
            tag: chip.tag,
        },
        success: function (resp) {
            Materialize.toast('已添加标签', 4000);
        },
        error: function () {
            Materialize.toast('添加标签失败', 4000);
        }
    });
}

// 删除标签
function deleteTags(e, chip) {
    $.ajax({
        type: 'DELETE',
        url: '/elebu/api/v1/tag/',
        data: {
            tag: chip.tag,
        },
        success: function (resp) {
            Materialize.toast('已删除标签', 4000);
        },
        error: function () {
            Materialize.toast('删除标签失败', 4000);
        }
    });
}

// 商家删除食物
function deleteFood(e) {
    let food_id = $(e.target).attr('food_id');
    $.ajax({
        type: 'DELETE',
        url: '/elebu/api/v1/food/',
        data: {
            food_id: food_id
        },
        success: function (resp) {
            if (resp['status'] === 200) {
                console.log(e.target);
                $(e.target).parent().parent().parent().remove();
                Materialize.toast('已下架菜品', 4000);
            } else {
                Materialize.toast('下架菜品失败', 4000);
            }
        },
        error: function () {
            Materialize.toast('下架菜品失败', 4000);
        }
    });
}

// 商家展示店内食物
function showFood(resp) {
    for (let i in resp['info']) {
        $('.belong').append(`<li>
                                <div class="collapsible-header">${resp['info'][i]['food_name']}<span class="new badge" data-badge-caption="">ID:${resp['info'][i]['food_id']}</span><span class="new badge" data-badge-caption="赞">${resp['info'][i]['zans']}</span></div>
                                <div class="collapsible-body">
                                    <p>${resp['info'][i]['food_desc']}</p>
                                        <div class="right-align">
                                            <a class="waves-effect waves-grey btn-flat" href="/user/food_photo/?food_id=${resp['info'][i]['food_id']}">上传图片</a>
                                            <a class="btn disabled"><b>${resp['info'][i]['food_price']}￥</b></a>
                                            <a class="waves-effect waves-grey btn-flat delfood" food_id="${resp['info'][i]['food_id']}">下架</a>
                                        </div>
                                </div>
                            </li>`);
    }
}

// 单家食物信息（获取全部食物，删除食物）
function foodInfo() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/food/',
        data: {
            num: 'self'
        },
        success: function (resp) {
            console.log(resp)
            showFood(resp)
            $('.delfood').click(function (e) {
                deleteFood(e);
            })
        },
        error: function () {
            console.log('失败惹');
        }
    });
}

// 展示个人的头像，用户名等基础信息
function showSelfInfo(resp) {
    let join_date = new Date(resp['join_time']);
    let now_date = new Date()
    // console.log(join_date)
    // console.log(now_date)
    let Difference_In_Time = now_date.getTime() - join_date.getTime();
	let Difference_In_Days = Difference_In_Time / (1000 * 3600 * 24);
    $('.avatar').attr('src', `/static/images/avatar/${resp['avatar']}`);
    $('.display-username').append(`${resp['username']}`);
    $('.selfintroduce-display').append(`<p >${resp['selfintroduce']}</p>`);
    $('#textarea1').val(`${resp['selfintroduce']}`);
    $('#textarea1').trigger('autoresize');
    $('.join-time').append(`${Math.floor(Difference_In_Days)}天`);
}

// 展示信息（基础信息，订单，商家食物，商家可接订单）
function selfInfo() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/selfinfo',
        data: {
            num: 'self'
        },
        success: function (resp) {
            let user_id = resp['user_id'];
            showSelfInfo(resp);
            let role = resp['role'];
            showOrders(user_id);
            if (role === 2) {
                showOrders(user_id, 'merchant');
                foodInfo();
            } else if (role === 3) {
                showOrders(user_id, 'rider');
            }
        }
    });
}

// 保存个人简介
function keepIntroduce() {
    $('.keep-introduce').click(function () {
        let introduce = $('#textarea1').val()
        $.ajax({
            type: 'put',
            url: '/elebu/api/v1/selfinfo/',
            data: {
                selfintroduce: introduce
            },
            success: function (resp) {
                if (resp.status === 200) {
                    $('.selfintroduce-display').empty();
                    $('.selfintroduce-display').append(`<b>个人介绍：</b><p>${introduce}</p>`);
                    Materialize.toast('已保存', 4000);
                } else {
                    Materialize.toast('保存失败', 4000);
                }
            },
            error: function () {
                Materialize.toast('保存失败', 4000);
            }
        });
    });
}

// 处理标签（获取标签，添加标签，删除标签）
function Tags() {
    getTags()
    $('.chips-initial').on('chip.add', function (e, chip) {
        addTags(e, chip);
    })
    $('.chips-initial').on('chip.delete', function (e, chip) {
        deleteTags(e, chip);
    });
}

function historyOrder() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/order/',
        data: {
            role: 'customer',
            user: 'self',
            arrive: 'arrive',
        },
        success: function (resp) {
            for (let i of resp['info']) {
                let zan = '<i class="material-icons tozan">thumb_up</i>';
                if (i['zan']) {
                    zan = '<i class="material-icons zaned">thumb_up</i>';
                }
                $('.history-order tbody').append(`<tr>
                                                      <td>${i['order_id']}</td>
                                                      <td>${i['order_date']}</td>
                                                      <td>${i['food_name']}</td>
                                                      <td>${i['food_count']}</td>
                                                      <td>${i['food_price']}</td>
                                                      <td food_id="${i['food_id']}">${zan}</td>
                                                  </tr>`);
            }
        },
        error: function () {

        }
    })
}

function zan() {
    let order_id = '';
    let food_id = '';
    let zan = '';
    $('.history-order').on('click', '.zaned', function (e) {
        order_id = $(e.target).parent().prev().prev().prev().prev().prev().text();
        food_id = $(e.target).parent().attr('food_id');
        zan = 'zaned';
        $.ajax({
        type: 'PUT',
        url: '/elebu/api/v1/zan/',
        data: {
            order_id: order_id,
            zan: zan,
            food_id: food_id
        },
        success: function (resp) {
            // console.log(resp)
            if(resp['status'] === 200){
                $(e.target).removeClass('zaned');
                $(e.target).addClass('tozan');
                Materialize.toast('取消点赞成功', 4000);
            }else{
                Materialize.toast('取消点赞失败', 4000);
            }
        },
        error: function () {
            Materialize.toast('取消点赞失败', 4000);
        }
    });
    })
    $('.history-order').on('click', '.tozan',function (e) {
        order_id = $(e.target).parent().prev().prev().prev().prev().prev().text();
        food_id = $(e.target).parent().attr('food_id');
        zan = 'tozan';
        $.ajax({
        type: 'PUT',
        url: '/elebu/api/v1/zan/',
        data: {
            order_id: order_id,
            zan: zan,
            food_id: food_id
        },
        success: function (resp) {
            if(resp['status'] === 200){
                $(e.target).removeClass('tozan');
                $(e.target).addClass('zaned');
                Materialize.toast('点赞成功', 4000);
            }else{
                Materialize.toast('点赞失败', 4000);
            }
        },
        error: function () {
            Materialize.toast('点赞失败', 4000);
        }
    });
    })
}
function followed() {
    $.ajax({
        url: '/elebu/api/v1/follow',
        type: 'GET',
        data: {
            follow_list: 'follow_list'
        },
        success: function (resp) {
            if(resp['status'] === 200){
                for(let i of resp['info']){
                    console.log(i);
                    $('#test3 .fl').append(`<div class="row">
                                            <div class="col s12 m12">
                                                <div class="card horizontal">
                                                    <div class="card-image">
                                                        <img class="merchant-img" src="/static/images/avatar/${i['merchant_avatar']}">
                                                    </div>
                                                    <div class="card-stacked">
                                                        <div class="card-content">
                                                            <h5>${i['merchant_name']}</h5>
                                                            <p class="merchant-introduce">${i['merchant_introduce']}</p>
                                                        </div>
                                                        <div class="card-action">
                                                            <a href="/shop/?merchant_id=${i['merchant_id']}">买点东西</a>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>`);
                }
            }
        }
    });
}
$(document).ready(function () {
    $('ul.tabs').tabs();
    historyOrder();
    selfInfo();
    Tags();
    keepIntroduce();
    zan();
    followed();
})
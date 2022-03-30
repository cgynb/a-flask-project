function getQueryVariable(variable) {
    var query = window.location.search.substring(1);
    var vars = query.split("&");
    for (var i = 0; i < vars.length; i++) {
        var pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    }
    return null;
}

function merchantInfo() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/selfinfo/',
        data: {
            num: 'one',
            merchant_id: getQueryVariable('merchant_id'),
        },
        success: function (resp) {
            $('.parallax img').attr('src', `/static/images/avatar/${resp['avatar']}`);
            $('.merchant-name').text(resp['username']);
        },
        error: function () {

        }
    });
}

function minus() {
    $('.minus').click(function () {
            if (Number($(this).next().text()) !== 0) {
                let foodId = $(this).next().attr('food_id');
                let n = Number($(this).next().text()) - 1;
                let foodPrice = $(this).next().next().next().text().replace('￥', '');
                let foodName = $(this).parent().prev().text();
                let total_price = Number($('#total-price').text().replace('￥', '')) - Number(foodPrice);
                $('#total-price').text(total_price + '￥');
                $(this).next().text(n);
                $(`#${foodId}`).remove();
                if (n) {
                    $('#order-list').append(`<tr id="${foodId}">
                                                        <td>${foodName}</td>
                                                        <td>${n}</td>
                                                        <td>${foodPrice}</td>
                                                     </tr>`);
                }
            }
        }
    );
}

function plus() {
    $('.plus').click(function () {
        let foodId = $(this).prev().attr('food_id');
        let n = Number($(this).prev().text()) + 1;
        let foodPrice = $(this).next().text().replace('￥', '');
        let foodName = $(this).parent().prev().text();
        let total_price = Number($('#total-price').text().replace('￥', '')) + Number(foodPrice);
        $('#total-price').text(total_price + '￥');
        $(this).prev().text(n);
        $(`#${foodId}`).remove();
        $('#order-list').append(`<tr id="${foodId}">
                                                    <td>${foodName}</td>
                                                    <td>${n}</td>
                                                    <td>${foodPrice}</td>
                                                 </tr>`);
    });
}

function checkout() {
    $('#total-price').click(function () {
        if (this.innerText !== '0￥') {
            let merchant_id = getQueryVariable('merchant_id');
            let datas = [];
            let order_list = $('#order-list').children();
            for (let i = 0; i < order_list.length; i++) {
                let data = {};
                data['merchant_id'] = merchant_id;
                data['food_id'] = $(order_list[i]).attr('id');
                let info = $(order_list[i]).children();
                for (let j = 0; j < info.length; j += 3) {
                    data['food_name'] = info[j].innerText;
                    data['food_count'] = info[j + 1].innerText;
                    data['food_price'] = info[j + 2].innerText;
                }
                datas.push(data);
            }
            $.ajax({
                type: 'POST',
                url: '/elebu/api/v1/order/',
                data: {data: JSON.stringify(datas)},
                success: function () {
                    Materialize.toast('购买成功', 4000);
                },
                error: function () {
                    Materialize.toast('购买失败', 4000);
                }
            });
        } else {
            Materialize.toast('您还没选择菜品', 4000);
        }
    });
}

function foodInfo(resp) {
    for (let i in resp['info']) {
        $('.food-list').append(`<li>
                                            <div class="collapsible-header">
                                                <span>${resp['info'][i]['food_name']}</span>
                                                <div class="right">
                                                    <a class="waves-effect waves-teal btn-flat minus">—</a>
                                                    <span class="price" food_id="${resp['info'][i]['food_id']}">0</span>
                                                    <a class="waves-effect waves-teal btn-flat plus">+</a>
                                                    <a class="btn disabled"><b>${resp['info'][i]['food_price']}￥</b></a>
                                                </div>
                                            </div>
                                            <div class="collapsible-body">
                                                <img class="food-img left-align" src="/static/images/food/${resp['info'][i]['address']}" alt="" onerror="this.src='/static/images/1.jpg'">
                                                <b><i class="material-icons">thumb_up</i>${resp['info'][i]['zans']}</b>
                                                <p>${resp['info'][i]['food_desc']}</p>
                                            </div>
                                        </li>`);
    }
}

function buy() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/food/',
        data: {
            merchant_id: getQueryVariable('merchant_id'),
        },
        success: function (resp) {
            foodInfo(resp);
            minus();
            plus();
        },
        error: function () {
            Materialize.toast('未知错误', 4000);
        }
    });
    checkout();
}

function follow() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/follow/',
        data: {
            followed_id: getQueryVariable('merchant_id')
        },
        success: function (resp) {
            if (resp['status'] === 200) {
                if (resp['info'] === 'followed') {
                    $('.follow').addClass('grey');
                    $('.follow').text('取消关注');
                }
            } else {
                Materialize.toast('请检查网络', 4000);
            }
        }
    });
    $('.follow').on('click', function () {
        let merchant_id = getQueryVariable('merchant_id');
        let type;
        if ($('.follow').hasClass('grey')) {
            type = 'DELETE';
        } else {
            type = 'POST';
        }
        $.ajax({
            type: type,
            url: '/elebu/api/v1/follow/',
            data: {
                followed_id: merchant_id,
            },
            success: function (resp) {
                if (resp['status'] === 200) {
                    if (type === 'POST') {
                        $('.follow').addClass('grey');
                        $('.follow').text('取消关注');
                        Materialize.toast('已关注', 4000);
                    } else if (type === 'DELETE') {
                        $('.follow').removeClass('grey');
                        $('.follow').text('关注');
                        Materialize.toast('取消关注', 4000);
                    }
                } else {
                    Materialize.toast('关注失败', 4000);
                }
            }
        });
    });
}

function getComment() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/comment/',
        data: {
            merchant_id: getQueryVariable('merchant_id')
        },
        success: function (resp) {
            let cmts = resp['info'];
            for (let cmt of cmts) {
                $('.comment-box').append(`
                                                <div class="row">
                                                <div class="col m11 s10 offset-m1 offset-s2">
                                                    <hr>
                                                </div>
                                                    <div class="col m1 s3">
                                                        <div class="col m12">
                                                            <img src="/static/images/avatar/${cmt['useravatar']}" onerror="this.src='/static/images/logo.jpg'" alt="" class="circle responsive-img">
                                                        </div>
                                                    </div>
                                                    <div class="col m11 s8">
                                                        <div class="row">
                                                            <b>${cmt['username']}</b>
                                                        </div>
                                                        <span class="black-text" id="${cmt['commentid']}">
                                                        ${cmt['comment']}
                                                      </span>
                                                        <a class="waves-effect waves-teal btn-flat right reply">回复</a>
                                                    </div>
                                                </div>
                                                `);
                for (let reply of cmt['replies']) {
                    $('.comment-box').append(`
                                    <div class="row">
                                        <div class="col m1 offset-m1 s3 offset-s1">
                                            <div class="col m10 s9">
                                                <img src="/static/images/avatar/${reply['useravatar']}" onerror="this.src='/static/images/logo.jpg'" alt="" class="circle responsive-img">
                                            </div>
                                        </div>
                                        <div class="col m10 s8">
                                            <div class="row">
                                                <b>${reply['username']}</b>
                                            </div>
                                            <div class="comment">
                                          <span class="black-text">
                                            ${reply['reply']}
                                          </span></div>
                                        </div>
                                    </div>`);
                }
            }
        },
    })
}

function reply() {
    $('.comment-box').on('click', '.reply', function () {
        if ($(this).parent().next()[0]) {
            $(this).text('回复');
            $(this).parent().next().remove();
        } else {
            $(this).text('收起');
            let comment_id = $(this).prev().attr('id');
            $(this).parent().parent().append(`
                                                <div class="row">
                                                    <form class="col s8 offset-s2">
                                                        <div class="row">
                                                            <div class="input-field col s10">
                                                                <textarea id="textarea1" class="materialize-textarea"></textarea>
                                                            </div>
                                                        </div>
                                                        <a class="waves-effect waves-light btn right send-reply" comment_id="${comment_id}">回复</a>
                                                    </form>
                                                </div>`)
        }
    });
    $('.comment-box').on('click', '.send-reply', function () {
        let self = $(this);
        $.ajax({
            type: 'POST',
            url: '/elebu/api/v1/comment/',
            data: {
                sub: $(this).attr('comment_id'),
                rpy: $(this).prev().children().children().val()
            },
            success: function (resp) {
                if (resp['status'] === 200) {
                    self.parent().parent().parent().append(`<div class="row">
                                        <div class="col m1 offset-m1 s3 offset-s1">
                                            <div class="col m10 s9">
                                                <img src="/static/images/avatar/${resp['data']['useravatar']}" onerror="this.src='/static/images/logo.jpg'" alt="" class="circle responsive-img">
                                            </div>
                                        </div>
                                        <div class="col m10 s8">
                                            <div class="row">
                                                <b>${resp['data']['username']}</b>
                                            </div>
                                            <div class="comment">
                                          <span class="black-text">
                                            ${resp['data']['reply']}
                                          </span></div>
                                        </div>
                                    </div>`);
                    self.parent().parent().remove();
                    Materialize.toast('评论成功', 4000);
                } else {
                    Materialize.toast('评论失败', 4000);
                }
            },
            error: function () {
                console.log('失败');
            }
        });

    });
}

function sendComment() {
    $('.send-comment').on('click', function () {
        $.ajax({
            type: 'POST',
            url: '/elebu/api/v1/comment/',
            data: {
                comment: $('#comment-textarea').val(),
                merchant_id: getQueryVariable('merchant_id')
            },
            success: function (resp) {
                if (resp['status'] === 200) {
                    $('#comment-textarea').val('');
                    Materialize.toast('评论成功', 4000);
                    $('.comment-box').append(`
                                                <div class="row">
                                                <div class="col m11 s10 offset-m1 offset-s2">
                                                    <hr>
                                                </div>
                                                    <div class="col m1 s3">
                                                        <div class="col m12">
                                                            <img src="/static/images/avatar/${resp['data']['useravatar']}" onerror="this.src='/static/images/logo.jpg'" alt="" class="circle responsive-img">
                                                        </div>
                                                    </div>
                                                    <div class="col m11 s8">
                                                        <div class="row">
                                                            <b>${resp['data']['username']}</b>
                                                        </div>
                                                        <span class="black-text" id="${resp['data']['commentid']}">
                                                        ${resp['data']['comment']}
                                                      </span>
                                                        <a class="waves-effect waves-teal btn-flat right reply">回复</a>
                                                    </div>
                                                </div>
                                                `);
                }
            },
            error: function () {

            }
        })
    })
}

function comment() {
    sendComment();
    getComment();
    reply();
}

$(document).ready(function () {
    $('.parallax').parallax();
    $('.modal').modal();
    merchantInfo();
    buy();
    follow();
    comment();
})
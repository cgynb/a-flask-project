function getFoodInfo() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/food/',
        data: {
            num: 'all'
        },
        success: function (resp) {
            for (let c of resp['info']) {
                $('#food').append(`<ul class="collection with-header" food_id="${c['foodid']}">
                                             <img class="col s1" src="/static/images/food/${c['photo']}" alt="阿偶" onerror="this.src='/static/images/1.jpg'">
                                             <li class="collection-item">图片：${c['photo']}<a class="right" del_thing="photo">删除</a></li>
                                             <li class="collection-item">商品名：${c['foodname']}<a class="right" del_thing="foodname">删除</a></li>
                                             <li class="collection-item">商品ID：${c['foodid']}</li>
                                             <li class="collection-item">商家ID：${c['merchantid']}</li>
                                             <li class="collection-item">介绍：${c['fooddesc']}<a class="right" del_thing="fooddesc">删除</a></li>
                                             <li class="collection-item"><a class="btn">过审</a></li>
                                           </ul>`)
            }
        }
    })
}

function FoodInfoEvent() {
    $('#food').on('click', 'a', function (e) {
        if ($(e.target).text() === '过审') {
            let food_id = $(e.target).parent().parent().attr('food_id');
            passFoodInfo(e.target, food_id);
        } else {
            let food_id = $(e.target).parent().parent().attr('food_id');
            let del_thing = $(e.target).attr('del_thing');
            delFoodInfo(e.target, food_id, del_thing);
        }
    })
}

function passFoodInfo(target, food_id) {
    $.ajax({
        type: 'put',
        url: '/elebu/api/v1/food/',
        data: {
            food_id: food_id,
            pass: 'pass'
        },
        success: function (resp) {
            if(resp['status'] === 200){
                $(target).parent().parent().remove();
            }else{
                Materialize.toast(resp['message'], 4000);
            }
        },
        error: function () {
            Materialize.toast('请检查网络', 4000);
        }
    })
}

function delFoodInfo(target, food_id, del_thing) {
    $.ajax({
        type: 'delete',
        url: '/elebu/api/v1/food/',
        data: {
            food_id: food_id,
            del_thing: del_thing
        },
        success: function (resp) {
            if (resp['status'] === 200) {
                if (del_thing === 'photo') {
                    $(target).parent().prev().attr('src', '/static/images/1.jpg');
                }
                let t = $(target).parent().text();
                $(target).parent().text(t.split('：')[0]);
            }else{
                Materialize.toast('something wrong', 4000);
            }
        },
        error: function () {
            Materialize.toast('请检查网络', 4000);
        }
    })
}

function getCommentInfo() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/comment/',
        data: {
            num: 'all'
        },
        success: function (resp) {
            for (let c of resp['info']) {
                $('#comment').append(`
                                                <div class="row">
                                                <hr>
                                                    <div class="col m11 s10 offset-m1 offset-s2">
                                                    <hr>
                                                </div>
                                                    <div class="col m1 s3">
                                                        <div class="col m12">
                                                            <img src="/static/images/avatar/${c['useravatar']}" onerror="this.src='/static/images/logo.jpg'" alt="" class="circle responsive-img">
                                                        </div>
                                                    </div>
                                                    <div class="col m11 s8">
                                                        <div class="row">
                                                            <b>${c['username']}</b>
                                                        </div>
                                                        <span class="black-text">
                                                            ${c['comment']}
                                                        </span>
                                                        <a class="waves-effect waves-teal btn-flat right del-cmt" cid="${c['commentid']}">删除</a>
                                                        <a class="waves-effect waves-teal btn-flat right pass-cmt" cid="${c['commentid']}">通过</a>
                                                    </div>
                                                </div>
                                                `);
                for (let reply of c['replies']) {
                    $('#comment').append(`
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
                                          </span>
                                          <a class="waves-effect waves-teal btn-flat right del-sub" sub_id="${reply['subid']}">删除</a>
                                          <a class="waves-effect waves-teal btn-flat right pass-sub" sub_id="${reply['subid']}">通过</a>
                                          </div>
                                        </div>
                                    </div>`);
                }
            }
        }
    })
}

function passComment(cmt_box, comment_type, comment_id) {
    $.ajax({
        type: 'put',
        url: '/elebu/api/v1/comment/',
        data: {
            comment_id: comment_id,
            comment_type: comment_type
        },
        success: function (resp) {
            if (resp.status === 200) {
                cmt_box.remove();
            } else {
                Materialize.toast(resp.message, 4000);
            }
        },
        error: function () {
            Materialize.toast('请检查网络', 4000)
        }
    });
}

function delComment(cmt_box, comment_type, comment_id) {
    $.ajax({
        type: 'delete',
        url: '/elebu/api/v1/comment/',
        data: {
            comment_id: comment_id,
            comment_type: comment_type
        },
        success: function (resp) {
            if (resp.status === 200) {
                cmt_box.remove();
            } else {
                Materialize.toast(resp.message, 4000);
            }
        },
        error: function () {
            Materialize.toast('请检查网络', 4000)
        }
    });
}

function delCommentBtn() {
    $('#comment').on('click', 'a.del-cmt', function (e) {
        delComment($(e.target).parent().parent(), 'comment', $(e.target).attr('cid'));
    })
    $('#comment').on('click', 'a.del-sub', function (e) {
        delComment($(e.target).parent().parent().parent(), 'subcomment', $(e.target).attr('sub_id'));
    })
}

function passCommentBtn() {
    $('#comment').on('click', 'a.pass-cmt', function (e) {
        passComment($(e.target).parent().parent(), 'comment', $(e.target).attr('cid'));
    })
    $('#comment').on('click', 'a.pass-sub', function (e) {
        passComment($(e.target).parent().parent().parent(), 'subcomment', $(e.target).attr('sub_id'));
    })
}

function getUserInfo() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/selfinfo/',
        data: {
            num: 'all'
        },
        success: function (resp) {
            if (resp['status'] === 200) {
                for (let c of resp['info']) {
                    let tags = '';
                    for (let t of c['tags']) {
                        tags += `<a del_thing="tag">${t}</a> `;
                    }
                    // $('#userinfo').append(JSON.stringify(c) + '<hr>');
                    $('#userinfo').append(`<ul class="collection with-header" user_id="${c['userid']}">
                                             <img class="col s1" src="/static/images/avatar/${c['avatar']}" alt="阿偶" onerror="this.src='/static/images/1.jpg'">
                                             <li class="collection-item">头像：${c['avatar']}<a class="right" del_thing="avatar">删除</a></li>
                                             <li class="collection-item">用户名：${c['username']}<a class="right" del_thing="username">删除</a></li>
                                             <li class="collection-item">用户ID：${c['userid']}</li>
                                             <li class="collection-item">介绍：${c['selfintroduce']}<a class="right" del_thing="selfintroduce">删除</a></li>
                                             <li class="collection-item">标签：${tags}</li>
                                             <li class="collection-item"><a class="btn">过审</a></li>
                                           </ul>`)
                }
            }
        }
    })
}

function delUserInfo(target, del_thing, user_id) {
    let del_thing_detail = null;
    if (del_thing === 'tag') {
        del_thing_detail = $(target).text();
    } else if (del_thing === 'avatar') {
        del_thing_detail = $(target).parent().prev().attr('src');
    }
    $.ajax({
        type: 'delete',
        url: '/elebu/api/v1/selfinfo/',
        data: {
            del_thing: del_thing,
            user_id: user_id,
            del_thing_detail: del_thing_detail
        },
        success: function (resp) {
            if (resp['status'] === 200) {
                if (del_thing === 'tag') {
                    $(target).remove();
                } else if (del_thing === 'avatar') {
                    $(target).parent().prev().attr('src', '/static/images/1.jpg');
                    let t = $(target).parent().text().split('：')[0];
                    $(target).parent().text(t + '：');
                } else if (del_thing === 'username' || $(target).attr('del_thing') === 'selfintroduce') {
                    let t = $(target).parent().text().split('：')[0];
                    $(target).parent().text(t + '：');
                }
            } else {
                Materialize.toast('删除失败', 4000);
            }
        },
        error: function () {
            Materialize.toast('请检查网络', 4000);
        }
    })
}

function passUserInfo(target, user_id) {
    $.ajax({
        type: 'put',
        url: '/elebu/api/v1/selfinfo/',
        data: {
            pass: 'pass',
            user_id: user_id
        },
        success: function (resp) {
            if (resp['status'] === 200) {
                $(target).parent().parent().remove();
            } else {
                Materialize.toast('过审失败，请刷新', 4000);
            }
        },
        error: function () {
            Materialize.toast('请检查网络', 4000);
        }
    })
}

function UserInfoEvent() {
    $('#userinfo').on('click', 'a', function (e) {
        if ($(e.target).text() === '过审') {
            passUserInfo(e.target, $(e.target).parent().parent().attr('user_id'));
        } else {
            delUserInfo(e.target, $(e.target).attr('del_thing'), $(e.target).parent().parent().attr('user_id'));
        }
    })
}

function post_notice() {
    $('.post-notice').click(function () {
        let title = $('.notice-title').val();
        let content = $('.notice-content').val();
        let date = $('.notice-date').val();
        $.ajax({
            type: 'POST',
            url: '/elebu/api/v1/notice/',
            data: {
                title: title,
                content: content,
                date: date
            },
            success: function (resp) {
                Materialize.toast('发布成功', 4000);
            }
        })
    })
}

$(document).ready(function () {
    $('input#input_text, textarea#textarea1').characterCounter();
    getFoodInfo();
    FoodInfoEvent();

    getCommentInfo();
    delCommentBtn();
    passCommentBtn();

    getUserInfo();
    UserInfoEvent();

    post_notice();
})
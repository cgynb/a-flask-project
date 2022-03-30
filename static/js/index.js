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

function merchantCard(resp) {
    for (let m in resp.merchants) {
        let m_id = resp.merchants[m]['merchant_id'];
        $.ajax({
            type: 'GET',
            url: '/elebu/api/v1/follow/',
            data: {
                merchant_id: m_id
            },
            success: function (r) {
                let f_num = r['follow-num'];
                $('.merchant-list').append(`<div class="col m3 s12">
                                                        <div class="card">
                                                            <div class="card-image waves-effect waves-block waves-light">
                                                                <img class="activator merchant-img" src="/static/images/avatar/${resp.merchants[m]['avatar']}" onerror="this.src='/static/images/2.jpg'">
                                                            </div>
                                                            <div class="card-content">
                                                                <span class="card-title activator grey-text text-darken-4">${resp.merchants[m]['username']}<i class="material-icons right">more_vert</i></span>
                                                            </div>
                                                            <p class="follow-num">${f_num}人关注</p>
                                                            <div class="card-reveal">
                                                                <span class="card-title grey-text text-darken-4">店家介绍<i
                                                                        class="material-icons right">close</i></span>
                                                                <p>${resp.merchants[m]['introduce']}</p>
                                                            </div>
                                                            <div class="card-action">
                                                                <a href="/shop/?merchant_id=${resp.merchants[m]['merchant_id']}">进店看看</a>
                                                            </div>
                                                        </div>
                                                    </div>`);
            }
        });
    }
}

function currentPage() {
    $('.pagination').click(function (e) {
        if (e.target.innerHTML != '...') {
            $.ajax({
                type: 'GET',
                url: '/elebu/api/v1/selfinfo',
                data: {
                    num: 'merchant',
                    page: e.target.innerHTML,
                    keyword: getQueryVariable('keyword')
                },
                success: function (resp) {
                    $('li.active.teal').removeClass('active teal');
                    $(e.target).parent().addClass('active teal');
                    $('.merchant-list').empty();
                    merchantCard(resp);
                },
                error: function () {
                    Materialize.toast('没有了哦', 4000);
                }
            });
        }
    });
}

function paginition() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/selfinfo',
        data: {
            num: 'merchant',
            page: 1,
            keyword: getQueryVariable('keyword')
        },
        success: function (resp) {
            merchantCard(resp);
            let total_page = resp['total_page'];
            let pag = ``;
            for (let i = 1; i <= total_page; i++) {
                if (i === 1) {
                    pag += `<li class="waves-effect active teal"><a href="#!">${i}</a></li>`;
                } else if (i > 2 && i < total_page - 1) {
                    pag += ``;
                } else if (i === total_page - 1) {
                    if (total_page >= 5) {
                        pag += `<li class=""><a href="#!">...</a></li>`;
                    }
                    pag += `<li class="waves-effect"><a href="#!">${i}</a></li>`;
                } else {
                    pag += `<li class="waves-effect"><a href="#!">${i}</a></li>`;
                }
            }
            $('.pagination').append(pag);
        },
        error: function () {

        }
    });
}

$(document).ready(function () {
    $('.slider').slider({full_width: true});
    paginition();
    currentPage();
});
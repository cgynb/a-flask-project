function getQueryVariable(variable) {
    let query = window.location.search.substring(1);
    let vars = query.split("&");
    for (let i = 0; i < vars.length; i++) {
        let pair = vars[i].split("=");
        if (pair[0] == variable) {
            return pair[1];
        }
    }
    return null;
}

function merchantCard(resp) {
    for (let m in resp['merchants']) {
        let m_id = resp['merchants'][m]['merchant_id'];
        $.ajax({
            type: 'GET',
            url: '/elebu/api/v1/follow/',
            data: {
                merchant_id: m_id
            },
            success: function (r) {
                let f_num = r['follow-num'];
                let t = '';
                let cnt = 0;
                for (let tag of resp['merchants'][m]['tags']) {
                    t += `<span class="new badge" data-badge-caption="${tag}"></span>`
                    cnt++;
                    if (cnt === 3) {
                        break;
                    }
                }
                $('.merchant-list').append(`<div class="col m3 s12">
                                                        <div class="card">
                                                            <div class="card-image waves-effect waves-block waves-light">
                                                                <img class="activator merchant-img" src="/static/images/avatar/${resp['merchants'][m]['avatar']}" onerror="this.src='/static/images/2.jpg'">
                                                            </div>
                                                            <div class="card-content">
                                                                <span class="card-title activator grey-text text-darken-4">${resp['merchants'][m]['username']}<i class="material-icons right">more_vert</i></span>
                                                            </div>
                                                            <div>标签：
                                                                <span class="new badge blue lighten-3" data-badge-caption="关注">${f_num}</span>
                                                                ${t}
                                                            </div>
                                                            <div class="card-reveal">
                                                                <span class="card-title grey-text text-darken-4">店家介绍<i
                                                                        class="material-icons right">close</i></span>
                                                                <p>${resp['merchants'][m]['introduce']}</p>
                                                            </div>
                                                            <div class="card-action">
                                                                <a href="/shop/?merchant_id=${resp['merchants'][m]['merchant_id']}">进店看看</a>
                                                            </div>
                                                        </div>
                                                    </div>`);
            }
        });
    }
}

function currentPage() {
    $('#pagination').click(function (e) {
        if (e.target.innerHTML !== '...') {
            $.ajax({
                type: 'GET',
                url: '/elebu/api/v1/selfinfo',
                data: {
                    num: 'merchant',
                    page: e.target.innerHTML,
                    keyword: getQueryVariable('keyword'),
                    tag: decodeURI(getQueryVariable('tag'))

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


function pagination() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/selfinfo',
        data: {
            num: 'merchant',
            page: 1,
            keyword: getQueryVariable('keyword'),
            tag: decodeURI(getQueryVariable('tag'))
        },
        success: function (resp) {
            merchantCard(resp);
            let total_page = resp['total_page'];
            let pag = ``;
            for (let i = 1; i <= total_page; i++) {
                if (i === 1) {
                    pag += `<li class="waves-effect active teal"><a>${i}</a></li>`;
                } else if (i > 2 && i < total_page - 1) {
                    pag += ``;
                } else if (i === total_page - 1) {
                    if (total_page >= 5) {
                        pag += `<li class=""><a>...</a></li>`;
                    }
                    pag += `<li class="waves-effect"><a>${i}</a></li>`;
                } else {
                    pag += `<li class="waves-effect"><a>${i}</a></li>`;
                }
            }
            $('#pagination').append(pag);
        },
        error: function () {

        }
    });
}

function get_notice() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/notice/',
        success: function (resp) {
            if (resp['status'] === 200) {
                $('.modal-content h4').text(resp['notice']['title']);
                $('.modal-content p').text(resp['notice']['content']);
                $('#notice').modal('open');
            }
        }
    })
}

function tag_classify() {
    let tag = getQueryVariable('tag');
    tag = decodeURI(tag);
    $(`a[href="?tag=${tag}"]`).parent().addClass('active teal lighten-3');
}

$(document).ready(function () {
    $('.slider').slider({full_width: true});
    tag_classify();
    pagination();
    currentPage();
    $('#notice').modal({
        starting_top: '0%',
        ending_top: '30%'
    });
    get_notice();
});
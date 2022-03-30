

function showChatList() {
    $.ajax({
        type: 'GET',
        url: '/elebu/api/v1/message/',
        data: {
            userid: userid
        },
        success: function (resp) {
            if(resp['status'] === 200){
                for(let i of resp['data']){
                    if(i['unread'] === 0){
                        $('.row').append(`   <div class="col s12 m8 offset-m2">
                            <div class="collection chat-list">
                                <a href="/chat/?orderid=${i['room']}" class="collection-item dismissable">
                                    <h6><b>订单号:${i['room']}</b></h6>
                                    <p class="grey-text">${i['last_msg_sender']}:${i['lastMsg']}</p>
                                </a>
                            </div>
                         </div>`);
                    }else {
                        $('.row').append(`   <div class="col s12 m8 offset-m2">
                            <div class="collection chat-list">
                                <a href="/chat/?orderid=${i['room']}" class="collection-item dismissable">
                                    <span class="new badge remind" data-badge-caption="未读">${i['unread']}</span>
                                    <h6><b>订单号:${i['room']}</b></h6>
                                    <p class="grey-text">${i['last_msg_sender']}:${i['lastMsg']}</p>
                                </a>
                            </div>
                         </div>`);
                    }
                }
            }else{
                Materialize.toast('something wrong', 4000);
            }
        },
        error: function () {
            Materialize.toast('请检查网络', 4000);
        }
    })
}


$(document).ready(function () {
    showChatList();
});

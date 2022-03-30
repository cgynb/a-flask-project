function send() {
    $('#captcha-btn').on('click', function () {
                let email = $('#email').val();
                $.ajax({
                    method: 'POST',
                    url: '/user/captcha/',
                    data: {
                        email: email
                    },
                    success: function (resp) {
                        Materialize.toast(resp.message, 4000);
                        if(resp.status === 200) {
                            $('#submit').removeClass('disabled');
                        }
                    },
                    error: function () {
                        Materialize.toast('发送失败', 4000);
                    }
                });
            });
}

$(document).ready(function () {
            $('select').material_select();
            send();
        });
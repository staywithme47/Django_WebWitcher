$(document).ready(function($) {
    let form = $('#next_action');
    console.log(form);


    form.on('submit', function (e) {
        e.preventDefault();
        console.log('123')
        var action = $('#action').val();
        console.log(action);
        save_action(action, is_delete = false)
    });

    function save_action(action, is_delete) {
        var data = {};
        data.action = action;
        var view_data;
        var csrf_token = $('#next_action [name="csrfmiddlewaretoken"]').val();
        data["csrfmiddlewaretoken"] = csrf_token;
        if (is_delete) {
            data["is_delete"] = true;
        }
        var url = form.attr("action");
        var msg = $('#message')
        console.log(data);

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: false,
            dataType:"json",
            success:function(data2) {
                console.log("OK2");
                console.log(data2.action);
                console.log(data2.message);
                console.log(data2.history);
                $('#info').load(document.URL +  ' #info');
                $('#turn').load(document.URL + ' #turn');
                // location.reload(true);
                $('#turnlog').html('<br>' + data2.history +' <br>');
                if (data2.message.length > 0){
                    window.alert(data2.message)
                    if (data2.message === 'game_ended') {
                        console.log(data2.win_witcher)
                        if (data2.win_witcher === 'witcher_wins') {
                            window.location.href = "/endgame?win=0"
                        }
                        else {
                            window.location.href = "/endgame?win=1"
                        }
                        console.log("check22")
                    }
                }

            },
            error: function () {
                console.log("error")
                console.log("message")
            }

        })
    };

});
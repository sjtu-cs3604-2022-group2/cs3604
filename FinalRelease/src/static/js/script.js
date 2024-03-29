$(document).ready(function () {
    // var socket = io.connect();
    var popupLoading = '<i class="notched circle loading icon green"></i> Loading...';
    var message_count = 0;
    var ENTER_KEY = 13;

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });

    function scrollToBottom() {
        var $messages = $('.messages');
        $messages.scrollTop($messages[0].scrollHeight);
    }

    var page = 1;

    function load_messages() {
        var $messages = $('.messages');
        var position = $messages.scrollTop();
        if (position === 0 && socket.nsp !== '/anonymous') {
            page++;
            $('.ui.loader').toggleClass('active');
            $.ajax({
                url: messages_url,
                type: 'GET',
                data: {page: page},
                success: function (data) {
                    var before_height = $messages[0].scrollHeight;
                    $(data).prependTo(".messages").hide().fadeIn(800);
                    var after_height = $messages[0].scrollHeight;
                    flask_moment_render_all();
                    $messages.scrollTop(after_height - before_height);
                    $('.ui.loader').toggleClass('active');
                    activateSemantics();
                },
                error: function () {
                    alert('No more messages.');
                    $('.ui.loader').toggleClass('active');
                }
            });
        }
    }

    $('.messages').off().scroll(load_messages);

    socket.on('user count', function (data) {
        $('#user-count').html(data.count);
    });

    socket.off('new message').on('new message', function (data) {
        message_count++;
        if (!document.hasFocus()) {
            document.title = '(' + message_count + ') ' + 'Chat';
        }
        if (data.user_id !== current_user_id) {
            messageNotify(data);
        }
        $('.messages').append(data.message_html);
        flask_moment_render_all();
        scrollToBottom();
        activateSemantics();
    });

    function new_message(e) {
        // e is the keydown event
        var $textarea = $('#message-textarea');
        var message_body = $textarea.val().trim();
        if (e.which === ENTER_KEY && !e.shiftKey && message_body) {
            e.preventDefault();
            socket.emit('new message', message_body);
            $textarea.val('')
        }
    }

    // submit message
     $('#message-textarea').on('keydown', new_message.bind(this));

    // submit snippet
    $('#snippet-button').on('click', function () {
        var $snippet_textarea = $('#message-textarea');
        var message = $snippet_textarea.val();
        if (message.trim() !== '') {
            socket.emit('new message', message);
            $snippet_textarea.val('')
        }
    });

    $('#pic-submit-btn').off('click').on('click', function () {
        var picform=$('#pic-form');
        var action_url=$(picform).prop('action');
        var input_area=$('#pic');
        var pic_input_file=$('#pic')[0].files[0];
        console.log(pic_input_file);//alert('111');
        var formdata=new FormData();
        formdata.append('pic',pic_input_file);
        $.ajax({
            type: "POST",//方法类型
            dataType: "json",//预期服务器返回的数据类型
            url: action_url ,//url
            data: formdata,
            contentType : false,
            processData : false,
            success: function (a) {
                var message=a['msg'];
                // alert(message);
                socket.emit('new message', message);
                // alert("HHHH");
                $(input_area).val('');
                //window.location.reload();
            },
            error : function() {alert('?????') ;}
        });
    });

    // open message modal on mobile
    $("#message-textarea").focus(function () {
        if (screen.width < 600) {
            $('#mobile-new-message-modal').modal('show');
            $('#mobile-message-textarea').focus()
        }
    });

    $('#send-button').on('click', function () {
        var $mobile_textarea = $('#mobile-message-textarea');
        var message = $mobile_textarea.val();
        if (message.trim() !== '') {
            socket.emit('new message', message);
            $mobile_textarea.val('')
        }
    });

    // quote message
    $('.right-msg').on('click', '.quote-button', function () {
        var $textarea = $('#message-textarea');
        var message = $(this).parent().parent().find('.msg-text').text();
        $textarea.val('> ' + message + '\n\n');
        $textarea.val($textarea.val()).focus()
    });


    function messageNotify(data) {
        if (Notification.permission !== "granted")
            Notification.requestPermission();
        else {
            var notification = new Notification("Message from " + data.nickname, {
                icon: data.gravatar,
                body: data.message_body.replace(/(<([^>]+)>)/ig, "")
            });

            notification.onclick = function () {
                window.open(root_url);
            };
            setTimeout(function () {
                notification.close()
            }, 4000);
        }
    }

    function activateSemantics() {
        $('.ui.dropdown').dropdown();
        //$('.ui.checkbox').checkbox();

        $('.message .close').on('click', function () {
            $(this).closest('.message').transition('fade');
        });

        $('#toggle-sidebar').on('click', function () {
            $('.menu.sidebar').sidebar('setting', 'transition', 'overlay').sidebar('toggle');
        });

        $('#show-help-modal').on('click', function () {
            $('.ui.modal.help').modal({blurring: true}).modal('show');
        });

        $('#show-snippet-modal').on('click', function () {
            $('.ui.modal.snippet').modal({blurring: true}).modal('show');
        });

        // $('.pop-card').popup({
        //     inline: true,
        //     on: 'hover',
        //     hoverable: true,
        //     html: popupLoading,
        //     delay: {
        //         show: 200,
        //         hide: 200
        //     },
        //     onShow: function () {
        //         var popup = this;
        //         popup.html(popupLoading);
        //         $.get({
        //             url: $(popup).prev().data('href')
        //         }).done(function (data) {
        //             popup.html(data);
        //         }).fail(function () {
        //             popup.html('Failed to load profile.');
        //         });
        //     }
        // });
    }

    function init() {
        scrollToBottom();
        // desktop notification
        document.addEventListener('DOMContentLoaded', function () {
            if (!Notification) {
                alert('Desktop notifications not available in your browser.');
                return;
            }

            if (Notification.permission !== "granted")
                Notification.requestPermission();
        });

        $(window).focus(function () {
            message_count = 0;
            document.title = 'Chat';
        });

        activateSemantics();
        
    }

    // delete message
    $('.right-msg').off('click', '.delete-button').on('click', '.delete-button', function () {
        var $this = $(this);
        $.ajax({
            type: 'DELETE',
            url: $this.parent().children(":first").val(),
            success: function () {
                $this.parent().parent().parent().remove();
            },
            error: function () {
                alert('Oops, something was wrong!')
            }
        });
    });

    // delete user
    $(document).on('click', '.delete-user-button', function () {
        var $this = $(this);
        $.ajax({
            type: 'DELETE',
            url: $this.data('href'),
            success: function () {
                alert('Success, this user is gone!')
            },
            error: function () {
                alert('Oops, something was wrong!')
            }
        });
    });

    init();

});
function scrollToBottom() {
    var $messages = $('.messages');
    $messages.scrollTop($messages[0].scrollHeight);
};
function showInputArea() {
    var btnobj=document.getElementById("btnobj");
    
    var shobj=document.getElementById("pic-input");
    if(shobj.value=="显示"){
        shobj.value="隐藏";
        shobj.style.display="none";
        btnobj.innerText="∨上传图片";

    }else{
        shobj.value="显示";
        shobj.style.display="block";
        btnobj.innerText="∧上传图片";
        scrollBy(0,document.body.scrollHeight);
    }
}
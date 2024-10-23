$(document).ready(function() {
    function scrollToBottom() {
        var chatBox = document.getElementById('chat-box');
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    $('#send-button').click(function() {
        var userMessage = $('#user-input').val();
        $('#chat-box').append('<div class="user-message">' + userMessage + '</div>');
        
        $('#chat-box').append('<div class="bot-typing">Bot is typing...</div>');
        
        $.ajax({
            url: '/chatbot',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ "message": userMessage }),
            success: function(response) {
                $('.bot-typing').remove();
                if (response.buttons) {
                    $('#button-responses').empty();
                    response.buttons.forEach(function(button) {
                        $('#button-responses').append('<button class="response-button">' + button + '</button>');
                    });
                } else {
                    $('#chat-box').append('<div class="bot-response">' + response.response + '</div>');
                }
                scrollToBottom();
            },
            error: function(xhr) {
                $('.bot-typing').remove();
                if (xhr.status === 404) {
                    $('#chat-box').append('<div class="error">Error: Not found.</div>');
                } else if (xhr.status === 500) {
                    $('#chat-box').append('<div class="error">Error: Server error.</div>');
                } else {
                    $('#chat-box').append('<div class="error">Error: Could not get response from the chatbot.</div>');
                }
                scrollToBottom();
            }
        });
        
        $('#user-input').val('');  // Clear input field
    });

    // Voice recognition
    $('#voice-button').click(function() {
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.onresult = function(event) {
            var voiceMessage = event.results[0][0].transcript;
            $('#user-input').val(voiceMessage);
            $('#send-button').click();
        };
        recognition.start();
    });

    // Theme toggle
    $('#theme-toggle').click(function() {
        $('body').toggleClass('dark-theme');
    });

    // Optional: Send message on pressing Enter key
    $('#user-input').keypress(function(event) {
        if (event.which === 13) {
            $('#send-button').click();
        }
    });
});

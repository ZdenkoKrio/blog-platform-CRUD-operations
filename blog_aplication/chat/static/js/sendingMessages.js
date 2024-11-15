document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const categoryName = chatLog.dataset.category;


    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + categoryName + '/'
    );


    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messageElement = document.createElement('p');
        messageElement.innerHTML = `
            <strong>${data.username}</strong>: ${data.message}
            <span class="timestamp">${data.timestamp}</span>
        `;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onopen = function() {
        console.log("The connection was setup successfully!");
    };

    chatSocket.onclose = function() {
        console.error('Chat socket closed unexpectedly');
    };


    const messageInputDom = document.querySelector('#chat-message-input');
    messageInputDom.focus();


    messageInputDom.addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            document.querySelector('#chat-message-submit').click();
        }
    });


    document.querySelector('#chat-message-submit').addEventListener('click', () => {
        const message = messageInputDom.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
        }
    });
});
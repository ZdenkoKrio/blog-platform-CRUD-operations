document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const chatType = chatLog.dataset.chatType;
    const chatId = chatLog.dataset.chatId;

    const chatSocket = new WebSocket(
        `ws://${window.location.host}/ws/chat/${chatType}/${chatId}/`
    );

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        const messageElement = document.createElement("div");
        messageElement.innerHTML = `
            <strong>${data.username}</strong>: ${data.message}
            <span style="font-size: 0.8em; color: gray;">(${data.timestamp})</span>
        `;
        chatLog.appendChild(messageElement);
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    document.getElementById("chat-message-submit").onclick = function () {
        const input = document.getElementById("chat-message-input");
        const message = input.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({ message }));
            input.value = "";
        }
    };
});
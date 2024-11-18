document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const chatType = chatLog.dataset.chatType;
    const chatId = chatLog.dataset.chatId;
    const messageInput = document.getElementById("chat-message-input");
    const messageSubmit = document.getElementById("chat-message-submit");

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

    messageSubmit.onclick = function () {
        const message = messageInput.value.trim();
        if (message) {
            chatSocket.send(JSON.stringify({ message }));
            messageInput.value = "";
        }
    };

    messageInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            messageSubmit.click();
        }
    });
});
document.addEventListener("DOMContentLoaded", () => {
    const chatLog = document.getElementById("chat-log");
    const chatType = chatLog.dataset.chatType;
    const chatId = chatLog.dataset.chatId;

    let offset = 0;
    const limit = 10;

    async function loadMessages() {
        try {
            const response = await fetch(`/chat/${chatType}/${chatId}/messages/?offset=${offset}`);
            if (!response.ok) throw new Error("Failed to load messages");

            const data = await response.json();
            const messages = data.messages;

            messages.forEach((msg) => {
                const messageElement = document.createElement("div");
                messageElement.innerHTML = `
                    <strong>${msg.sender}:</strong> ${msg.message}
                    <span style="font-size: 0.8em; color: gray;">(${msg.timestamp})</span>
                `;
                chatLog.prepend(messageElement);
            });

            offset += limit;
        } catch (error) {
            console.error("Error loading messages:", error);
        }
    }

    chatLog.addEventListener("scroll", () => {
        if (chatLog.scrollTop === 0) loadMessages();
    });

    loadMessages();
});
document.addEventListener("DOMContentLoaded", () => {
    let offset = 0;
    const limit = 10;
    const chatLog = document.getElementById("chat-log");
    const category = chatLog.dataset.category;

    async function loadMessages() {
        try {
            const response = await fetch(`/chat/${category}/messages/?offset=${offset}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            const messages = data.messages;

            messages.forEach((message) => {
                const messageElement = document.createElement("div");
                messageElement.innerHTML = `
                    <strong>${message.sender}:</strong> ${message.message}
                    <span style="font-size: 0.8em; color: gray;">(${message.timestamp})</span>
                `;
                chatLog.prepend(messageElement);
            });

            offset += limit;
        } catch (error) {
            console.error("Error loading messages:", error);
        }
    }

    loadMessages();

    chatLog.addEventListener("scroll", () => {
        if (chatLog.scrollTop === 0) {
            loadMessages();
        }
    });
});
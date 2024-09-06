document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.getElementById("send-button");
    const userMessageInput = document.getElementById("user-message");
    const chatBody = document.getElementById("chat-body");

    if (sendButton && userMessageInput && chatBody) {
        sendButton.addEventListener("click", function() {
            const message = userMessageInput.value.trim();
            if (message) {
                const userMessageElement = document.createElement("div");
                userMessageElement.className = "chat-message user-message";
                userMessageElement.textContent = message;
                chatBody.appendChild(userMessageElement);

                userMessageInput.value = "";

                fetch(`/chatgpt/weather-chat/?message=${encodeURIComponent(message)}`, {
                    method: "GET",  // Ensure GET method
                    headers: {
                        "Content-Type": "application/json",
                    },
                })
                .then(response => response.json())
                .then(data => {
                    const botMessageElement = document.createElement("div");
                    botMessageElement.className = "chat-message bot-message";
                    botMessageElement.textContent = data.message || 'No message received';
                    chatBody.appendChild(botMessageElement);
                    
                    chatBody.scrollTop = chatBody.scrollHeight;
                })
                .catch(error => {
                    console.error("Error:", error);
                });
            }
        });
    }
});

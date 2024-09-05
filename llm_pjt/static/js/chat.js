document.addEventListener("DOMContentLoaded", function() {
    // Get the elements
    const sendButton = document.getElementById("send-button");
    const userMessageInput = document.getElementById("user-message");
    const chatBody = document.getElementById("chat-body");

    if (sendButton && userMessageInput && chatBody) {
        sendButton.addEventListener("click", function() {
            const message = userMessageInput.value.trim();
            if (message) {
                // Append the user's message to the chat body
                const userMessageElement = document.createElement("div");
                userMessageElement.className = "chat-message user-message";
                userMessageElement.textContent = message;
                chatBody.appendChild(userMessageElement);

                // Clear the input field
                userMessageInput.value = "";

                // Send the message to the server
                fetch("/chatgpt/weather-chat/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken") // Get CSRF token for POST requests
                    },
                    body: JSON.stringify({ message: message })
                })
                .then(response => response.json())
                .then(data => {
                    const botMessageElement = document.createElement("div");
                    botMessageElement.className = "chat-message bot-message";
                    botMessageElement.textContent = data.message;
                    chatBody.appendChild(botMessageElement);
                    
                    // Scroll to the bottom of the chat body
                    chatBody.scrollTop = chatBody.scrollHeight;
                })
                .catch(error => {
                    console.error("Error:", error);
                });
            }
        });
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

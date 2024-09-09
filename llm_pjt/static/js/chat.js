document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.getElementById("send-button");
    const userMessageInput = document.getElementById("user-message");
    const chatBody = document.getElementById("chat-body");

    function sendMessage() {
        const message = userMessageInput.value.trim();
        if (message) {
            // 메시지가 이미 전송되었는지 확인
            if (userMessageInput.dataset.sending === "true") return;
            userMessageInput.dataset.sending = "true";

            const userMessageElement = document.createElement("div");
            userMessageElement.className = "chat-message user-message";
            userMessageElement.textContent = message;
            chatBody.appendChild(userMessageElement);

            userMessageInput.value = "";

            // 로딩 메시지 타이머 설정
            let loadingMessageElement;
            const loadingMessageTimeout = setTimeout(() => {
                loadingMessageElement = document.createElement("div");
                loadingMessageElement.className = "chat-message bot-message";
                loadingMessageElement.textContent = "잠시만요. 날씨 정보를 찾는 중입니다.⏳";
                chatBody.appendChild(loadingMessageElement);

                chatBody.scrollTop = chatBody.scrollHeight;
            }, 1500); // 1.5초 후 로딩 메시지 표시

            // 응답을 기다립니다
            fetch(`/chatgpt/weather-chat/?message=${encodeURIComponent(message)}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                // 타이머 정리 및 로딩 메시지 제거
                clearTimeout(loadingMessageTimeout);
                if (loadingMessageElement) {
                    chatBody.removeChild(loadingMessageElement);
                }

                // 실제 응답 메시지를 추가합니다
                const botMessageElement = document.createElement("div");
                botMessageElement.className = "chat-message bot-message";
                botMessageElement.textContent = data.message || 'No message received';
                chatBody.appendChild(botMessageElement);

                chatBody.scrollTop = chatBody.scrollHeight;
            })
            .catch(error => {
                // 타이머 정리 및 로딩 메시지 제거
                clearTimeout(loadingMessageTimeout);
                if (loadingMessageElement) {
                    chatBody.removeChild(loadingMessageElement);
                }

                console.error("Error:", error);

                const errorMessageElement = document.createElement("div");
                errorMessageElement.className = "chat-message bot-message";
                errorMessageElement.textContent = "응답을 받는 중 오류가 발생했습니다.";
                chatBody.appendChild(errorMessageElement);

                chatBody.scrollTop = chatBody.scrollHeight;
            })
            .finally(() => {
                userMessageInput.dataset.sending = "false";
            });
        }
    }

    if (sendButton && userMessageInput && chatBody) {
        sendButton.addEventListener("click", sendMessage);

        // 엔터 키를 눌렀을 때 메시지 전송
        userMessageInput.addEventListener("keydown", function(event) {
            if (event.key === "Enter") {
                event.preventDefault(); // 기본 엔터 키 동작 방지
                sendMessage();
            }
        });
    }
});

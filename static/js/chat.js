let chatSocket = null;
let chatVisible = true;

function initChat() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    chatSocket = new WebSocket(protocol + '//' + window.location.host + '/ws/chat/');
    
    const messagesDiv = document.getElementById('chat-messages');
    const input = document.getElementById('chat-input');
    
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messageDiv = document.createElement('div');
        messageDiv.innerHTML = `<strong>${data.usuario}:</strong> ${data.mensagem} <small class="text-muted">${new Date(data.timestamp).toLocaleTimeString()}</small>`;
        messagesDiv.appendChild(messageDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    };
    
    if (input) {
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && input.value.trim()) {
                chatSocket.send(JSON.stringify({'mensagem': input.value}));
                input.value = '';
            }
        });
    }
}

document.addEventListener('DOMContentLoaded', function() {
    initChat();
    
    const chatHeader = document.getElementById('chat-header');
    if (chatHeader) {
        chatHeader.onclick = function() {
            const body = document.getElementById('chat-body');
            chatVisible = !chatVisible;
            body.style.display = chatVisible ? 'block' : 'none';
        };
    }
});
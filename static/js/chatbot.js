document.addEventListener("DOMContentLoaded", function() {
    const toggleBtn = document.getElementById('chatbot-toggle');
    const popup = document.getElementById('chatbot-popup');
    const closeBtn = document.getElementById('chatbot-close');
    const sendBtn = document.getElementById('chatbot-send');
    const inputField = document.getElementById('chatbot-input');
    const messagesBox = document.getElementById('chatbot-messages');

    // Generate or fetch Session ID
    let sessionId = localStorage.getItem('taskmates_chat_session');
    if (!sessionId) {
        sessionId = 'sess_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('taskmates_chat_session', sessionId);
    }

    // Toggle Chat visibility
    toggleBtn.addEventListener('click', () => {
        popup.classList.toggle('d-none');
        if(!popup.classList.contains('d-none')) {
            inputField.focus();
        }
    });

    closeBtn.addEventListener('click', () => popup.classList.add('d-none'));

    function appendMessage(text, isUser) {
        const div = document.createElement('div');
        div.className = `bubble ${isUser ? 'user-message' : 'bot-message'}`;
        div.textContent = text;
        messagesBox.appendChild(div);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function showTyping() {
        const div = document.createElement('div');
        div.className = 'typing-indicator bot-message';
        div.id = 'typing';
        div.innerHTML = '<span></span><span></span><span></span>';
        messagesBox.appendChild(div);
        messagesBox.scrollTop = messagesBox.scrollHeight;
    }

    function hideTyping() {
        const typingItem = document.getElementById('typing');
        if(typingItem) typingItem.remove();
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    async function handleSend() {
        const text = inputField.value.trim();
        if (!text) return;

        appendMessage(text, true);
        inputField.value = '';
        showTyping();

        try {
            const response = await fetch('/chatbot/query/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    session_id: sessionId,
                    message: text
                })
            });
            const data = await response.json();
            hideTyping();
            if(data.response) {
                appendMessage(data.response, false);
            } else {
                appendMessage("Sorry, I encountered an error.", false);
            }
        } catch (err) {
            console.error(err);
            hideTyping();
            appendMessage("Unable to reach the server. Please check your connection.", false);
        }
    }

    sendBtn.addEventListener('click', handleSend);
    inputField.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') handleSend();
    });
});

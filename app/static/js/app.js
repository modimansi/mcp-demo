document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const resetButton = document.getElementById('reset-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    let messages = [];
    
    // Show loading indicator
    function showLoading() {
        loadingIndicator.style.display = 'block';
        messageInput.disabled = true;
        chatForm.querySelector('button').disabled = true;
    }
    
    // Hide loading indicator
    function hideLoading() {
        loadingIndicator.style.display = 'none';
        messageInput.disabled = false;
        chatForm.querySelector('button').disabled = false;
        messageInput.focus();
    }
    
    // Add a message to the chat
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        
        if (role === 'user') {
            messageDiv.classList.add('user-message');
        } else if (role === 'assistant') {
            messageDiv.classList.add('assistant-message');
        } else {
            messageDiv.classList.add('system-message');
        }
        
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        
        // Auto scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add to messages array
        if (role === 'user' || role === 'assistant') {
            messages.push({ role, content });
        }
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Add user message to the chat
        addMessage('user', message);
        messageInput.value = '';
        
        // Show loading indicator
        showLoading();
        
        try {
            // Send the message to the API
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    messages: messages,
                    stream: false
                })
            });
            
            if (!response.ok) {
                throw new Error('Error sending message');
            }
            
            const data = await response.json();
            
            // Add assistant message to the chat
            addMessage('assistant', data.message.content);
            
        } catch (error) {
            console.error('Error:', error);
            addMessage('system', 'An error occurred. Please try again.');
        } finally {
            // Hide loading indicator
            hideLoading();
        }
    });
    
    // Handle reset button
    resetButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/reset');
            if (response.ok) {
                // Clear chat messages
                chatMessages.innerHTML = '';
                messages = [];
                addMessage('system', 'Conversation has been reset.');
            }
        } catch (error) {
            console.error('Error resetting conversation:', error);
            addMessage('system', 'Failed to reset conversation.');
        }
    });
    
    // Add initial system message
    addMessage('system', 'Welcome to MCP Demo! How can I help you today?');
});

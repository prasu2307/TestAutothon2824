"""
Web Interface for AI Test Chatbot using Flask
"""
from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot_engine import TestChatBot

app = Flask(__name__)
chatbot = TestChatBot()

@app.route('/')
def index():
    """Main chatbot interface"""
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Process chat messages"""
    user_message = request.json.get('message', '')
    
    if user_message.lower() == 'help':
        response = chatbot.get_help()
    else:
        response = chatbot.process_command(user_message)
    
    return jsonify({
        'response': response,
        'status': 'success'
    })

@app.route('/history')
def history():
    """Get conversation history"""
    return jsonify(chatbot.get_conversation_summary())

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # Create basic HTML template
    html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Test Chatbot</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .chat-container { max-width: 800px; margin: 0 auto; }
        .chat-box { height: 400px; border: 1px solid #ccc; padding: 10px; overflow-y: scroll; }
        .input-container { margin-top: 10px; }
        .input-container input { width: 70%; padding: 10px; }
        .input-container button { width: 25%; padding: 10px; }
        .message { margin: 10px 0; }
        .user-message { text-align: right; color: blue; }
        .bot-message { text-align: left; color: green; white-space: pre-line; }
    </style>
</head>
<body>
    <div class="chat-container">
        <h1>🤖 AI Test Chatbot - TestAutothon2824</h1>
        <div id="chatBox" class="chat-box"></div>
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your command here..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage('You: ' + message, 'user-message');
            input.value = '';

            fetch('/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                addMessage('🤖 Bot: ' + data.response, 'bot-message');
            });
        }

        function addMessage(message, className) {
            const chatBox = document.getElementById('chatBox');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + className;
            messageDiv.textContent = message;
            chatBox.appendChild(messageDiv);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        // Initial help message
        addMessage('🤖 Bot: Welcome! Type "help" for available commands or start with "Run UI tests"', 'bot-message');
    </script>
</body>
</html>
    '''
    
    with open(os.path.join(templates_dir, 'chatbot.html'), 'w') as f:
        f.write(html_template)
    
    print("🚀 Starting AI Test Chatbot Web Interface...")
    print("📱 Open http://localhost:5000 in your browser")
    app.run(debug=True, port=5000)
"""
Quick launcher for AI Test Chatbot
"""
import sys
import os

# Add the AIChatbotOrchestrator to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'AIChatbotOrchestrator'))

from AIChatbotOrchestrator.chatbot_engine import TestChatBot


def demo_chatbot():
    """Demo the chatbot functionality"""
    chatbot = TestChatBot()
    
    print("🤖 AI Test Chatbot Demo - TestAutothon2824 Framework")
    print("=" * 60)
    
    # Demo commands
    demo_commands = [
        "Run UI tests on Chrome",
        "Execute visual tests",
        "Optimize flaky tests",
        "Analyze API test results",
        "Speed up test execution"
    ]
    
    for command in demo_commands:
        print(f"\\n👤 User: {command}")
        response = chatbot.process_command(command)
        print(f"🤖 Bot: {response}")
        print("-" * 40)


def interactive_mode():
    """Interactive chatbot mode"""
    chatbot = TestChatBot()
    
    print("🤖 AI Test Chatbot - Interactive Mode")
    print("=" * 50)
    print("Type 'help' for commands, 'demo' for demo, or 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("👋 Goodbye!")
                break
            
            if user_input.lower() == 'demo':
                demo_chatbot()
                continue
            
            if user_input.lower() == 'help':
                print(chatbot.get_help())
                continue
            
            if not user_input:
                continue
            
            response = chatbot.process_command(user_input)
            print(f"🤖 Bot: {response}")
            print()
            
        except KeyboardInterrupt:
            print("\\n👋 Goodbye!")
            break


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'demo':
        demo_chatbot()
    else:
        interactive_mode()
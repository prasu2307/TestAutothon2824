"""
Command Line Interface for AI Test Chatbot
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot_engine import TestChatBot


def main():
    """Main CLI interface for the chatbot"""
    chatbot = TestChatBot()
    
    print("🤖 AI Test Chatbot - TestAutothon2824 Framework")
    print("=" * 50)
    print("Type 'help' for available commands or 'quit' to exit")
    print()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Happy testing!")
                break
            
            if user_input.lower() == 'help':
                print(chatbot.get_help())
                continue
            
            if not user_input:
                continue
            
            # Process the command
            print("🤖 Bot:", end=" ")
            response = chatbot.process_command(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\\n👋 Goodbye! Happy testing!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()


if __name__ == "__main__":
    main()
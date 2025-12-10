#!/usr/bin/env python3
"""
Telegram Message Sender
Reads text from a .txt file and sends it to a Telegram chat via a bot.
"""

import sys
import os
import requests


def read_text_file(filepath: str) -> str:
    """Read text content from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content.strip()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)


def send_telegram_message(bot_token: str, chat_id: str, message: str) -> bool:
    """
    Send a message to Telegram chat using bot API.
    
    Args:
        bot_token: Telegram bot token
        chat_id: Telegram chat ID (can be user ID or chat ID)
        message: Message text to send
    
    Returns:
        True if successful, False otherwise
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"  # Optional: allows basic HTML formatting
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            print(f"✓ Message sent successfully to chat {chat_id}")
            return True
        else:
            print(f"✗ Error: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error sending message: {e}")
        return False


def main():
    """Main function."""
    if len(sys.argv) < 4:
        print("Usage: python telegram_sender.py <bot_token> <chat_id> <text_file.txt>")
        print("\nExample:")
        print("  python telegram_sender.py 123456:ABC-DEF1234ghIkl -1001234567890 message.txt")
        print("\nTo get bot token:")
        print("  1. Talk to @BotFather on Telegram")
        print("  2. Create a new bot with /newbot")
        print("  3. Copy the token provided")
        print("\nTo get chat ID:")
        print("  1. Add your bot to the chat or start a conversation")
        print("  2. Send a message to the bot")
        print("  3. Visit: https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates")
        print("  4. Find 'chat':{'id': <CHAT_ID>} in the response")
        sys.exit(1)
    
    bot_token = sys.argv[1]
    chat_id = sys.argv[2]
    text_file = sys.argv[3]
    
    # Validate file exists
    if not os.path.exists(text_file):
        print(f"Error: File '{text_file}' does not exist.")
        sys.exit(1)
    
    # Read text from file
    print(f"Reading text from '{text_file}'...")
    message_text = read_text_file(text_file)
    
    if not message_text:
        print("Warning: File is empty. Nothing to send.")
        sys.exit(0)
    
    print(f"Message length: {len(message_text)} characters")
    print(f"Sending to chat {chat_id}...")
    
    # Send message
    success = send_telegram_message(bot_token, chat_id, message_text)
    
    if success:
        print("Done!")
        sys.exit(0)
    else:
        print("Failed to send message.")
        sys.exit(1)


if __name__ == "__main__":
    main()


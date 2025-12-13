# Telegram Integration - Instructions

## Example
Telegram Bot Username: @diamond_xyz_bot 
python telegram_sender.py chatid:token 8282579559 message.txt

## Installation

1. Install Python 3.6 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

### Step 1: Create a Telegram Bot

1. Open Telegram and search for **@BotFather**
2. Start a conversation and send `/newbot`
3. Follow the instructions to name your bot
4. BotFather will give you a **bot token** (looks like: `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
5. **Save this token** - you'll need it to run the script

### Step 2: Get Your Chat ID

There are two ways to get your chat ID:

#### Option A: For Private Chats (Direct Messages)
1. Start a conversation with your bot (search for your bot's username)
2. Send any message to the bot (e.g., "Hello")
3. Open this URL in your browser (replace `YOUR_BOT_TOKEN` with your actual token):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
4. Look for `"chat":{"id":123456789}` in the JSON response
5. The number after `"id":` is your chat ID

#### Option B: For Group Chats
1. Add your bot to the group
2. Send a message in the group
3. Visit the same URL as above: `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
4. Find the chat ID in the response (group IDs are usually negative numbers like `-1001234567890`)

## Usage

### Create a Text File

Create a `.txt` file with the content you want to send:

**Example: `message.txt`**
```
Hello! This is a test message from the Telegram bot.
This text was read from a file and sent automatically.
```

### Run the Script

```bash
python telegram_sender.py <BOT_TOKEN> <CHAT_ID> <TEXT_FILE.txt>
```

**Example:**
```bash
python telegram_sender.py 123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11 123456789 message.txt
```

## Example Workflow

1. Create `message.txt`:
   ```
   This is my outreach message.
   It can be multiple lines.
   ```

2. Run the script:
   ```bash
   python telegram_sender.py YOUR_BOT_TOKEN YOUR_CHAT_ID message.txt
   ```

3. Check your Telegram chat - the message should appear!

## Troubleshooting

- **"Unauthorized" error**: Check that your bot token is correct
- **"Chat not found" error**: 
  - Make sure you've started a conversation with the bot (for private chats)
  - Make sure the bot is added to the group (for group chats)
  - Verify the chat ID is correct
- **"File not found"**: Check that the file path is correct

## Notes

- The script reads the entire file content and sends it as one message
- Telegram has a message length limit of 4096 characters
- For longer messages, consider splitting the file or using file upload instead
- No UI needed - it's a simple command-line script


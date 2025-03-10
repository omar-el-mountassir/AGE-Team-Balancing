# Installation Guide for Age of Empires 2 Team Balancing Bot

This guide provides detailed instructions for installing and setting up the Age of Empires 2 Team Balancing Bot on different platforms.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation on Windows](#installation-on-windows)
- [Installation on macOS](#installation-on-macos)
- [Installation on Linux](#installation-on-linux)
- [Discord Bot Setup](#discord-bot-setup)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Troubleshooting](#troubleshooting)
- [Updating](#updating)

## Prerequisites

Before you begin, ensure you have the following:

- Python 3.8 or higher installed
- Git (optional, for cloning the repository)
- A Discord account with administrative access to a Discord server
- Basic understanding of command line operations

## Installation on Windows

### 1. Install Python

1. Download Python from [python.org](https://www.python.org/downloads/windows/)
2. Run the installer and check "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```
   python --version
   ```

### 2. Install Git (Optional)

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Run the installer with default settings
3. Verify installation by opening Command Prompt and typing:
   ```
   git --version
   ```

### 3. Get the Bot Code

Option A (with Git):

```
git clone https://github.com/yourusername/AGE-Team-Balancing.git
cd AGE-Team-Balancing
```

Option B (without Git):

1. Download the ZIP file from the GitHub repository
2. Extract the ZIP file to a folder
3. Open Command Prompt and navigate to the extracted folder:
   ```
   cd path\to\AGE-Team-Balancing
   ```

### 4. Set Up a Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 5. Install Dependencies

```
pip install -r requirements.txt
```

## Installation on macOS

### 1. Install Python

1. Install Homebrew if not already installed:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```
   brew install python
   ```
3. Verify installation:
   ```
   python3 --version
   ```

### 2. Install Git (Optional)

```
brew install git
```

### 3. Get the Bot Code

Option A (with Git):

```
git clone https://github.com/yourusername/AGE-Team-Balancing.git
cd AGE-Team-Balancing
```

Option B (without Git):

1. Download the ZIP file from the GitHub repository
2. Extract the ZIP file to a folder
3. Open Terminal and navigate to the extracted folder:
   ```
   cd path/to/AGE-Team-Balancing
   ```

### 4. Set Up a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

### 5. Install Dependencies

```
pip install -r requirements.txt
```

## Installation on Linux

### 1. Install Python and Git

For Debian/Ubuntu:

```
sudo apt update
sudo apt install python3 python3-pip python3-venv git
```

For Fedora:

```
sudo dnf install python3 python3-pip python3-virtualenv git
```

Verify installations:

```
python3 --version
git --version
```

### 2. Get the Bot Code

Option A (with Git):

```
git clone https://github.com/yourusername/AGE-Team-Balancing.git
cd AGE-Team-Balancing
```

Option B (without Git):

1. Download the ZIP file from the GitHub repository
2. Extract the ZIP file to a folder
3. Open Terminal and navigate to the extracted folder:
   ```
   cd path/to/AGE-Team-Balancing
   ```

### 3. Set Up a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```
pip install -r requirements.txt
```

## Discord Bot Setup

Before running the bot, you need to create a bot application on Discord:

### 1. Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" tab and click "Add Bot"
4. Under the bot's username, click "Reset Token" and copy the token (you'll need this later)

### 2. Configure Bot Permissions

1. Under "Privileged Gateway Intents", enable:
   - Server Members Intent
   - Message Content Intent
2. Under "Bot Permissions", select:
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use Slash Commands

### 3. Invite the Bot to Your Server

1. Go to the "OAuth2" > "URL Generator" tab
2. In the "Scopes" section, select:
   - bot
   - applications.commands
3. In the "Bot Permissions" section, select the permissions from step 2
4. Copy the generated URL and open it in your browser
5. Select your server from the dropdown and click "Authorize"

## Configuration

### 1. Create a Configuration File

Copy the example configuration file:

```
cp .env.example .env
```

### 2. Edit the Configuration

Open the `.env` file in a text editor and set at least the following:

```
# Required
DISCORD_TOKEN=your_discord_bot_token_here

# Optional but recommended
COMMAND_PREFIX=!
BOT_STATUS=Balancing AoE2 Teams
```

Replace `your_discord_bot_token_here` with the token you copied from the Discord Developer Portal.

### 3. Additional Configuration (Optional)

Review and modify other settings in the `.env` file as needed. See the file comments for details on each setting.

## Running the Bot

### Start the Bot

With the virtual environment activated:

```
python main.py
```

You should see log messages indicating that the bot is starting up and connecting to Discord.

### Verify the Bot is Working

1. In your Discord server, check if the bot is online
2. Try a simple command like `/help` or `/status`

### Running in the Background (Linux/macOS)

To keep the bot running after you close the terminal:

1. Install screen or tmux:

   ```
   # Debian/Ubuntu
   sudo apt install screen

   # Fedora
   sudo dnf install screen
   ```

2. Start a screen session:

   ```
   screen -S aoe2bot
   ```

3. Activate the virtual environment and start the bot:

   ```
   source venv/bin/activate
   python main.py
   ```

4. Detach from the screen session by pressing `Ctrl+A` followed by `D`

5. To reattach later:
   ```
   screen -r aoe2bot
   ```

## Troubleshooting

### Bot Doesn't Start

1. Check your Python version:

   ```
   python --version  # or python3 --version on Unix systems
   ```

   Must be 3.8 or higher.

2. Verify that all dependencies are installed:

   ```
   pip install -r requirements.txt
   ```

3. Check your Discord token in the `.env` file

4. Check the error messages in the console

### Bot Doesn't Respond to Commands

1. Make sure the bot is online in your Discord server
2. Check that you've enabled the correct intents in the Discord Developer Portal
3. Verify the bot has the necessary permissions in your server
4. Check if you're using slash commands correctly (they start with `/`)

### API Connection Issues

1. Check your internet connection
2. Verify the API base URLs in your `.env` file
3. The APIs might be temporarily unavailable

## Updating

To update the bot to the latest version:

1. Stop the bot (press `Ctrl+C` in the terminal window)
2. Pull the latest changes (if using Git):

   ```
   git pull
   ```

   Or download and extract the latest version

3. Update dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Start the bot again:
   ```
   python main.py
   ```

---

If you encounter problems not covered in this guide, please check the [Troubleshooting section of the README](../README.md#troubleshooting) or open an issue on GitHub.

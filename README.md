# Age of Empires 2 Team Balancing Bot

A Discord bot for creating balanced teams for Age of Empires 2 multiplayer games, taking into account player ELO ratings, position preferences, and suggesting optimal civilizations.

_Read this in [Français](README-fr.md)_

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.3.0%2B-blue)](https://discordpy.readthedocs.io/en/stable/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## Overview

This bot helps Age of Empires 2 communities create fair and balanced teams for multiplayer matches. It's especially useful for communities with players of varying skill levels (ELO ratings ranging from 1100 to 2400).

### Key Features

- **Player Registration**: Register players with their Steam nicknames and automatically fetch their ELO ratings
- **Team Balancing**: Generate balanced team compositions based on player ELO and preferences
- **Position Optimization**: Suggest optimal positions (flank/pocket) for players based on their performance history
- **Civilization Suggestions**: Recommend civilizations based on position, map, and team composition
- **Match History**: Track game results and maintain statistics for players
- **API Resilience**: Fallback mechanisms to handle API unavailability

## Installation

### Prerequisites

- Python 3.8 or higher
- A Discord bot token from [Discord Developer Portal](https://discord.com/developers/applications)
- Access to the Discord server where you want to add the bot
- Git (optional, for cloning the repository)

### Setup Guide

1. **Get the code**:

   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/AGE-Team-Balancing.git
   cd AGE-Team-Balancing

   # Alternatively, download and extract the ZIP file from GitHub
   ```

2. **Set up a virtual environment**:

   ```bash
   # Create a virtual environment
   python -m venv venv

   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot**:

   ```bash
   # Create a configuration file
   cp .env.example .env
   ```

   Then edit the `.env` file with your settings. At minimum, you need to set:

   - `DISCORD_TOKEN`: Your Discord bot token from the Discord Developer Portal

5. **Run the bot**:

   ```bash
   python main.py
   ```

### Discord Bot Setup

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Navigate to the "Bot" tab and click "Add Bot"
4. Under "Privileged Gateway Intents", enable:
   - Server Members Intent
   - Message Content Intent
5. Under "Token", click "Copy" to copy your bot token (this goes in your `.env` file)
6. To add the bot to your server, go to the "OAuth2" > "URL Generator" tab
7. Select the "bot" and "applications.commands" scopes
8. Select the following bot permissions:
   - Read Messages/View Channels
   - Send Messages
   - Embed Links
   - Attach Files
   - Read Message History
   - Use Slash Commands
9. Copy the generated URL and open it in your browser to add the bot to your server

## Configuration

The bot is configured through environment variables in the `.env` file. Here's what each setting means:

### Discord Bot Configuration

- `DISCORD_TOKEN`: Your Discord bot token
- `COMMAND_PREFIX`: Prefix for bot commands (default: `!`)
- `BOT_STATUS`: Status message displayed for the bot

### API Configuration

- `AOE2_GG_API_BASE_URL`: Base URL for the aoe2.gg API
- `AOE_NEXUS_API_BASE_URL`: Base URL for the AOE Nexus API
- `AOCREC_API_BASE_URL`: Base URL for the AOCREC API
- `API_TIMEOUT`: Timeout in seconds for API requests
- `API_CACHE_TTL`: Time-to-live in seconds for cached API responses

### Database Configuration

- `DATABASE_URL`: Database connection string (default uses SQLite)

### Team Balancing Configuration

- `ELO_1V1_WEIGHT`: Weight given to 1v1 ELO ratings (0-1)
- `ELO_TEAM_WEIGHT`: Weight given to team ELO ratings (0-1)
- `POSITION_FACTOR_MIN`: Minimum adjustment factor for position preferences
- `POSITION_FACTOR_MAX`: Maximum adjustment factor for position preferences
- `ACCEPTABLE_TEAM_DIFF_PERCENT`: Maximum acceptable percentage difference between teams

### Additional Settings

- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)
- `LOG_FORMAT`: Logging format (console or json)
- `DEV_MODE`: Enable development mode features
- `ENABLE_ML_BALANCER`: Enable machine learning balancer (if implemented)

## Usage

### Basic Commands

- `/register [steam_nickname]` - Register yourself with your Steam nickname
- `/profile [user?]` - View your profile or another user's profile
- `/queue [position_preference?]` - Join the queue for a game
- `/leave` - Leave the queue
- `/status` - Check the current queue status
- `/balance [2v2|3v3|4v4]` - Generate balanced team compositions

### Advanced Commands

- `/preferences [flank|pocket] [civilizations?]` - Set your position and civilization preferences
- `/civ_suggest [position] [map?]` - Get civilization suggestions
- `/report_result [win|loss]` - Report the result of a game
- `/stats [player?]` - View player statistics
- `/history` - View previous team compositions

### Admin Commands

- `/admin_update_elo [user]` - Force update of a player's ELO ratings
- `/admin_force [user] [team]` - Force a player into a specific team
- `/admin_config [setting] [value?]` - View or modify bot configuration
- `/admin_status` - View bot status
- `/clear_queue` - Clear the queue

## Troubleshooting

### Common Issues

1. **Bot doesn't respond to commands**:

   - Check if the bot is online in Discord
   - Verify that you've enabled the correct intents in the Discord Developer Portal
   - Ensure the bot has proper permissions in your server

2. **API errors when fetching ELO ratings**:

   - Check your internet connection
   - Verify the API base URLs in your `.env` file
   - The APIs might be temporarily unavailable; the bot has fallback mechanisms

3. **Bot crashes on startup**:
   - Check your Discord token
   - Ensure all dependencies are correctly installed
   - Review the error logs for specific issues

### Getting Help

If you encounter issues not covered here, please:

1. Check the logs for error messages
2. Open an issue on GitHub with details about your problem
3. Include relevant error messages and your configuration (remove sensitive information)

## Development

### Project Structure

```tree
/AGE-Team-Balancing
  /src
    /api           - API clients for fetching player data
    /balancer      - Team balancing algorithms
    /models        - Data models
    /data          - Static data (civilizations, maps)
    /bot           - Discord bot implementation
    /utils         - Utility functions
    /services      - Additional services
  /tests           - Test suite
  main.py          - Entry point
  config.py        - Configuration
  requirements.txt - Dependencies
```

### Running Tests

```bash
pytest
```

### Code Style

This project follows PEP 8 style guidelines. You can check your code style with:

```bash
flake8 .
```

And format your code with:

```bash
black .
```

## Future Development

Our roadmap includes:

1. **Database Integration**: Replace in-memory storage with a persistent database
2. **Advanced Metrics**: Implement more sophisticated player performance tracking
3. **Machine Learning Balancer**: Use ML to predict game outcomes and create balanced teams
4. **Web Interface**: Develop a companion web app for easier interaction
5. **Internationalization**: Add support for multiple languages
6. **Voice Channel Management**: Automatically move players to team voice channels

See the `project-plan.md` file for more details on future development.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for more detailed information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) for the Discord API wrapper
- [AoE2.net](https://aoe2.net/) for the Age of Empires 2 API
- The Age of Empires 2 community for inspiration and support

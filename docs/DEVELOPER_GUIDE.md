# Age of Empires 2 Team Balancing Bot - Developer Guide

This guide is intended for developers who want to understand the bot's architecture, extend its functionality, or contribute to the project.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Bot Commands](#bot-commands)
- [Data Flow](#data-flow)
- [API Integration](#api-integration)
- [Team Balancing Algorithm](#team-balancing-algorithm)
- [Civilization Selection](#civilization-selection)
- [Adding New Features](#adding-new-features)
- [Testing](#testing)
- [Deployment](#deployment)

## Architecture Overview

The bot is built with a modular architecture, separating different concerns into distinct components:

- **Discord Integration**: Handles interactions with the Discord API
- **API Clients**: Fetch player data from external Age of Empires 2 APIs
- **Data Models**: Define the core entities (Players, Teams, etc.)
- **Balancing Logic**: Implements algorithms for creating balanced teams
- **Civilization Logic**: Suggests optimal civilizations based on various factors
- **Storage**: Handles persistence (currently in-memory, planned to be database-backed)

The system is designed to be asynchronous, leveraging Python's `asyncio` and Discord.py's event-driven nature.

## Project Structure

```
/AGE-Team-Balancing/
  /src/                  # Source code
    /api/                # API clients for external services
    /balancer/           # Team balancing algorithms
    /bot/                # Discord bot implementation
      /cogs/             # Discord command groups
    /data/               # Static data (civilizations, maps)
    /models/             # Data models
    /services/           # Additional services
    /utils/              # Utility functions
  /tests/                # Test suite
    /unit/               # Unit tests
    /integration/        # Integration tests
    /mocks/              # Mock objects for testing
  main.py                # Entry point
  config.py              # Configuration management
```

## Core Components

### 1. Data Models (`src/models/`)

- **Player**: Represents a Discord user with their AoE2 information (ELO ratings, preferences)
- **Team**: A collection of players with positions and civilizations
- **Civilization**: Detailed information about a civilization, including strengths and ratings
- **GameResult**: Records the outcome of a match

### 2. API Clients (`src/api/`)

- **APIClientInterface**: Common interface for all API clients
- **AoE2GGClient**: Client for the AoE2.GG API
- **APIFactory**: Factory and fallback mechanism for API clients

### 3. Balancing Logic (`src/balancer/`)

- **TeamBalancer**: Generates balanced team compositions
- **PositionAnalyzer**: Analyzes optimal positions for players
- **CivilizationBalancer**: Suggests optimal civilizations

### 4. Discord Bot (`src/bot/`)

- **AGETeamBalancer**: Main bot class
- **Registration Cog**: Commands for player registration and profiles
- **Balancing Cog**: Commands for team balancing and queuing
- **Stats Cog**: Commands for statistics and history
- **Admin Cog**: Administrative commands

## Bot Commands

The bot uses Discord's slash commands, implemented using the `app_commands` module from discord.py.

Each command follows this basic structure:

```python
@app_commands.command(name="command_name", description="Command description")
@app_commands.describe(param1="Description of parameter 1")
async def command_name(self, interaction: discord.Interaction, param1: str):
    # Implementation
    await interaction.response.send_message("Response")
```

### Adding a New Command

1. Identify the appropriate cog for your command
2. Add your command method following the above pattern
3. Handle the command logic, performing necessary operations
4. Send an appropriate response to the user

## Data Flow

### Team Balancing Flow

1. User registers with a Steam nickname
2. Bot fetches ELO ratings from external APIs
3. User joins the queue
4. Admin initiates team balancing
5. Balancing algorithm creates team compositions
6. Team compositions are presented to the user
7. User selects a composition
8. Game result is recorded

## API Integration

The bot can integrate with multiple APIs to fetch player data:

1. **Primary API**: AoE2.GG for player ratings
2. **Fallback APIs**: Additional APIs can be implemented and will be used as fallbacks

### Implementing a New API Client

1. Create a new class in `src/api/` that implements `APIClientInterface`
2. Implement all required methods
3. Add the new client to the `APIFactory`

## Team Balancing Algorithm

The core balancing algorithm operates as follows:

1. Calculate a score for each player based on:

   - 1v1 ELO (weighted by `ELO_1V1_WEIGHT`)
   - Team ELO (weighted by `ELO_TEAM_WEIGHT`)
   - Position preference adjustment
   - Historical performance adjustment

2. Generate all possible team combinations

3. For each combination:

   - Assign positions to players (respecting preferences if possible)
   - Calculate team scores
   - Calculate the difference between team scores
   - Score the composition based on balance and novelty

4. Return the top N compositions

## Civilization Selection

The civilization suggestion algorithm considers:

1. Position-specific tier ratings
2. Map-specific ratings
3. Player preferences
4. Synergies with teammates
5. Counters to enemy civilizations

## Adding New Features

### Step 1: Design

1. Define the feature's requirements and scope
2. Identify which components need to be modified
3. Design the necessary data structures and algorithms
4. Plan the user interface (commands, options, responses)

### Step 2: Implementation

1. Create or modify the necessary data models
2. Implement the core logic
3. Create Discord commands to expose the functionality
4. Add appropriate documentation

### Step 3: Testing

1. Write unit tests for the core logic
2. Test the Discord commands manually
3. Add integration tests if necessary

## Testing

The project uses pytest for testing. There are several categories of tests:

- **Unit Tests**: Test individual functions and classes
- **Integration Tests**: Test interactions between components
- **Bot Tests**: Test Discord command functionality

### Writing Tests

1. Create a test file in the appropriate directory
2. Import the component to test
3. Write test functions prefixed with `test_`
4. Use assertions to verify behavior

Example:

```python
def test_team_balancer_creates_balanced_teams():
    # Arrange
    balancer = TeamBalancer()
    players = [...]  # Create test players

    # Act
    compositions = balancer.generate_team_compositions(players, team_size=2)

    # Assert
    assert len(compositions) > 0
    assert len(compositions[0]) == 2  # Two teams
    # Check balance
    team_scores = [balancer.calculate_team_score(team) for team in compositions[0]]
    score_diff = abs(team_scores[0] - team_scores[1])
    assert score_diff / sum(team_scores) * 100 < config.ACCEPTABLE_TEAM_DIFF_PERCENT
```

## Deployment

The bot can be deployed in several ways:

### Local Deployment

1. Clone the repository
2. Install dependencies
3. Configure the `.env` file
4. Run `python main.py`

### Docker Deployment

A Dockerfile will be added in the future for containerized deployment.

### Hosted Deployment

The bot can be deployed to cloud services like:

- Heroku
- AWS
- Google Cloud
- Any VPS provider

Key considerations for deployment:

- Persistent storage for player data
- Network access for API calls
- Memory requirements (depends on the number of players and servers)
- CPU requirements (for team balancing algorithm)

## Future Development

See the project plan for detailed information on planned features:

- Database integration
- Machine learning for team balancing
- Web interface
- Internationalization
- Voice channel integration

---

This developer guide provides an overview of the bot's architecture and how to extend it. For questions not covered here, please refer to the source code or ask in the project's GitHub repository.

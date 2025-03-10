# Age of Empires 2 Team Balancing Bot - User Guide

Welcome to the Age of Empires 2 Team Balancing Bot user guide! This document will explain how to use the bot to create balanced teams for your Age of Empires 2 games.

## Table of Contents

- [Getting Started](#getting-started)
- [Basic Commands](#basic-commands)
- [Game Workflow](#game-workflow)
- [Player Settings](#player-settings)
- [Team Balancing](#team-balancing)
- [Game Results and Statistics](#game-results-and-statistics)
- [Admin Commands](#admin-commands)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Inviting the Bot

The bot needs to be invited to your Discord server by someone with administrative permissions. If the bot is not already in your server, contact your server administrator.

### Registration

Before you can use the bot, you need to register with your Steam nickname. This allows the bot to fetch your ELO ratings from Age of Empires 2 rating services.

```
/register <steam_nickname>
```

Example:

```
/register TheViper
```

The bot will fetch your ELO ratings and confirm your registration. If your ratings can't be found, you'll still be registered but without ratings.

## Basic Commands

Here are the essential commands you'll use:

- `/register <steam_nickname>` - Register with your Steam nickname
- `/profile [user?]` - View your profile or another user's profile
- `/queue [position_preference?]` - Join the queue for a game
- `/leave` - Leave the queue
- `/status` - Check the current queue status
- `/balance <team_size>` - Generate balanced teams (e.g., `/balance 2` for 2v2)
- `/report_result <winning_team> <map_name> [game_duration?]` - Report a game result

## Game Workflow

The typical workflow for organizing a game is:

1. Players register using `/register` (only needed once)
2. Players join the queue using `/queue`
3. When enough players are in the queue, an organizer uses `/balance` to create teams
4. Players review the suggested team compositions
5. Once a composition is selected, players join their respective teams
6. After the game, someone reports the result using `/report_result`

## Player Settings

### Viewing Your Profile

To see your profile, use:

```
/profile
```

This shows your ELO ratings, preferred position, preferred civilizations, and game statistics.

To view another player's profile:

```
/profile @PlayerName
```

### Setting Preferences

You can set your preferred position (flank or pocket) and preferred civilizations:

```
/preferences <position> [civilizations?]
```

Examples:

```
/preferences flank
/preferences pocket britons,mayans,ethiopians
/preferences any franks,berbers
```

### Updating ELO Ratings

If you want to update your ELO ratings:

```
/update
```

## Team Balancing

### Joining the Queue

To join the queue for a game:

```
/queue [position_preference?]
```

The optional position preference will override your default preference just for this game.

Examples:

```
/queue
/queue flank
/queue pocket
```

### Checking Queue Status

To see who's in the queue:

```
/status
```

### Leaving the Queue

If you need to leave the queue:

```
/leave
```

### Creating Balanced Teams

When enough players are in the queue, an organizer can create balanced teams:

```
/balance <team_size> [respect_preferences?]
```

Examples:

```
/balance 2  # For 2v2 games
/balance 3  # For 3v3 games
/balance 4  # For 4v4 games
```

The bot will suggest up to three different team compositions. Click on the buttons to select a composition.

## Game Results and Statistics

### Reporting Game Results

After a game, report the result:

```
/report_result <winning_team> <map_name> [game_duration?]
```

Examples:

```
/report_result 1 arabia  # Team 1 won on Arabia
/report_result 2 arena 45  # Team 2 won on Arena, game lasted 45 minutes
```

### Viewing Game History

To see recent game results:

```
/history [count?]
```

Example:

```
/history 10  # Show the last 10 games
```

### Viewing Player Statistics

To see detailed statistics for yourself or another player:

```
/stats [user?]
```

### Viewing Leaderboard

To see the server leaderboard:

```
/leaderboard [metric?] [position?]
```

Examples:

```
/leaderboard  # Default sorts by win rate
/leaderboard games_played  # Sort by number of games played
/leaderboard win_rate flank  # Show win rates for the flank position
```

## Civilization Suggestions

To get civilization suggestions for a specific position and map:

```
/civ_suggest <position> [map?]
```

Examples:

```
/civ_suggest flank
/civ_suggest pocket arabia
```

## Admin Commands

These commands are only available to server administrators:

- `/admin_update_elo <user>` - Force update of a player's ELO ratings
- `/admin_force <user> <team>` - Force a player into a specific team
- `/admin_config <setting> [value?]` - View or modify bot configuration
- `/admin_status` - View bot status
- `/clear_queue` - Clear the queue

## Best Practices

1. **Register with your correct Steam nickname** to ensure accurate ELO ratings
2. **Set your position preferences** to help create more balanced teams
3. **Report all game results** to build up statistics and improve team balancing
4. **Don't leave the queue** without using the `/leave` command
5. **Join the queue only when you're ready** to play a game
6. **Consider the suggested civilizations** for your position and the map

## Troubleshooting

### Common Issues

1. **Bot doesn't respond to commands**:

   - Make sure you're using slash commands (starting with `/`)
   - Check if the bot is online in your server
   - Verify that the bot has the necessary permissions

2. **ELO ratings not found**:

   - Double-check your Steam nickname spelling
   - Your profile might not be indexed by the rating services
   - Try using `/update` to refresh your ratings

3. **Team balancing seems unfair**:
   - Make sure all players have registered and have ELO ratings
   - The bot balances teams based on available data
   - Report game results to improve future balancing

### Getting Help

If you encounter issues not covered in this guide:

1. Ask an administrator in your Discord server
2. Check the project's GitHub repository for updates or known issues
3. Report the issue to the bot developer with details about what happened

---

We hope this guide helps you get the most out of the Age of Empires 2 Team Balancing Bot! Good luck and have fun with your balanced games!

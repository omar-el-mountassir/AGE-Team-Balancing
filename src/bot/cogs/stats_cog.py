"""
Stats Cog for the Age of Empires 2 Team Balancing Bot.
Handles statistics, history, and game results.
"""

from datetime import datetime
from typing import Dict, List, Optional, Set

import discord
from discord import app_commands
from discord.ext import commands

import config
from src.models.game_result import GameResult
from src.models.player import Player, Position
from src.models.team import Team
from src.utils.logger import get_logger

logger = get_logger(__name__)

class StatsCog(commands.Cog):
    """
    Cog for handling statistics, history, and game results.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the stats cog.
        
        Args:
            bot: The Discord bot instance.
        """
        self.bot = bot
        
        # In-memory storage for game history (would be replaced with a database in production)
        self.game_history = []  # List of GameResult objects
    
    @app_commands.command(name="report_result", description="Report the result of a game")
    @app_commands.describe(
        winning_team="The number of the winning team",
        map_name="The name of the map played",
        game_duration="The duration of the game in minutes (optional)"
    )
    async def report_result(
        self, 
        interaction: discord.Interaction, 
        winning_team: int,
        map_name: str,
        game_duration: Optional[int] = None
    ):
        """
        Report the result of a game.
        
        Args:
            interaction: The Discord interaction.
            winning_team: The number of the winning team.
            map_name: The name of the map played.
            game_duration: The duration of the game in minutes.
        """
        # Get the balancing cog to access team compositions
        balancing_cog = self.bot.get_cog("BalancingCog")
        if not balancing_cog:
            await interaction.response.send_message(
                "Balancing system is not available.",
                ephemeral=True
            )
            return
        
        # Check if there are any current compositions
        if not balancing_cog.current_compositions:
            await interaction.response.send_message(
                "No team compositions are currently available. Generate teams first with `/balance`.",
                ephemeral=True
            )
            return
        
        # Get the first composition (most recently generated)
        composition = balancing_cog.current_compositions[0]
        
        # Check if the winning team number is valid
        if winning_team < 1 or winning_team > len(composition):
            await interaction.response.send_message(
                f"Invalid team number. Must be between 1 and {len(composition)}.",
                ephemeral=True
            )
            return
        
        # Create a game result
        game_result = GameResult(
            teams=composition,
            map_name=map_name,
            game_mode="Random Map",  # Default game mode
            game_type=f"{len(composition[0].members)}v{len(composition[0].members)}",
            winning_team_index=winning_team - 1,
            game_duration_minutes=game_duration,
            reported_by=interaction.user.id
        )
        
        # Add to history
        self.game_history.append(game_result)
        
        # Update player statistics
        registration_cog = self.bot.get_cog("RegistrationCog")
        if registration_cog:
            for player_data in game_result.get_all_players():
                discord_id, _, position_str, civilization, won = player_data
                
                if discord_id in registration_cog.players:
                    player = registration_cog.players[discord_id]
                    position = Position.from_string(position_str)
                    
                    player.record_game_result(won, position, civilization)
        
        # Create an embed with the game result
        embed = discord.Embed(
            title="Game Result Reported",
            description=game_result.get_team_composition_description(),
            color=discord.Color.green()
        )
        
        if game_duration:
            embed.add_field(name="Duration", value=f"{game_duration} minutes", inline=True)
        
        embed.add_field(name="Map", value=map_name, inline=True)
        embed.add_field(name="Reported By", value=f"<@{interaction.user.id}>", inline=True)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="history", description="View game history")
    @app_commands.describe(count="The number of games to show (default: 5)")
    async def history(self, interaction: discord.Interaction, count: int = 5):
        """
        View game history.
        
        Args:
            interaction: The Discord interaction.
            count: The number of games to show.
        """
        if not self.game_history:
            await interaction.response.send_message(
                "No game history available.",
                ephemeral=True
            )
            return
        
        # Limit count to a reasonable number
        count = min(count, 10)
        
        # Get the most recent games
        recent_games = self.game_history[-count:]
        
        # Create embeds for each game
        embeds = []
        
        for i, game in enumerate(reversed(recent_games)):
            embed = discord.Embed(
                title=f"Game {len(self.game_history) - i}",
                description=game.get_team_composition_description(),
                color=discord.Color.blue(),
                timestamp=game.created_at
            )
            
            if game.game_duration_minutes:
                embed.add_field(name="Duration", value=f"{game.game_duration_minutes} minutes", inline=True)
            
            embed.add_field(name="Map", value=game.map_name, inline=True)
            
            if game.reported_by:
                embed.add_field(name="Reported By", value=f"<@{game.reported_by}>", inline=True)
            
            embeds.append(embed)
        
        # Send the embeds
        for embed in embeds:
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="stats", description="View player statistics")
    @app_commands.describe(user="The user to view statistics for (leave empty for your own statistics)")
    async def stats(self, interaction: discord.Interaction, user: discord.User = None):
        """
        View player statistics.
        
        Args:
            interaction: The Discord interaction.
            user: The user to view statistics for. If None, view the caller's statistics.
        """
        target_user = user or interaction.user
        discord_id = target_user.id
        
        # Get the registration cog to access player data
        registration_cog = self.bot.get_cog("RegistrationCog")
        if not registration_cog:
            await interaction.response.send_message(
                "Registration system is not available.",
                ephemeral=True
            )
            return
        
        # Check if player is registered
        if discord_id not in registration_cog.players:
            await interaction.response.send_message(
                f"{target_user.name} is not registered.",
                ephemeral=True
            )
            return
        
        player = registration_cog.players[discord_id]
        
        # Create an embed with player statistics
        embed = discord.Embed(
            title=f"Statistics: {player.discord_name}",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Games Played", value=player.games_played, inline=True)
        embed.add_field(name="Games Won", value=player.games_won, inline=True)
        embed.add_field(name="Win Rate", value=f"{player.get_win_rate():.1f}%", inline=True)
        
        # Add position-specific stats
        flank_games = player.position_performance[Position.FLANK]["games"]
        pocket_games = player.position_performance[Position.POCKET]["games"]
        
        if flank_games > 0:
            flank_win_rate = player.get_position_win_rate(Position.FLANK)
            embed.add_field(name="Flank Stats", value=f"{flank_games} games, {flank_win_rate:.1f}% win rate", inline=True)
        
        if pocket_games > 0:
            pocket_win_rate = player.get_position_win_rate(Position.POCKET)
            embed.add_field(name="Pocket Stats", value=f"{pocket_games} games, {pocket_win_rate:.1f}% win rate", inline=True)
        
        # Add civilization stats
        if player.civ_performance:
            # Sort civilizations by number of games played
            sorted_civs = sorted(
                player.civ_performance.items(),
                key=lambda x: x[1]["games"],
                reverse=True
            )
            
            # Show the top 5 most played civilizations
            top_civs = sorted_civs[:5]
            
            civ_text = ""
            for civ, stats in top_civs:
                games = stats["games"]
                wins = stats["wins"]
                win_rate = (wins / games) * 100 if games > 0 else 0
                civ_text += f"{civ}: {games} games, {win_rate:.1f}% win rate\n"
            
            if civ_text:
                embed.add_field(name="Top Civilizations", value=civ_text, inline=False)
        
        # Add recent games
        recent_games = []
        for game in reversed(self.game_history):
            for player_data in game.get_all_players():
                game_discord_id, _, _, civ, won = player_data
                if game_discord_id == discord_id:
                    result = "Won" if won else "Lost"
                    recent_games.append(f"{result} on {game.map_name} with {civ}")
                    break
            
            if len(recent_games) >= 5:
                break
        
        if recent_games:
            embed.add_field(name="Recent Games", value="\n".join(recent_games), inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="leaderboard", description="View the leaderboard")
    @app_commands.describe(
        metric="The metric to sort by (win_rate, games_played, games_won)",
        position="Filter by position (flank, pocket, any)"
    )
    async def leaderboard(
        self, 
        interaction: discord.Interaction, 
        metric: str = "win_rate",
        position: str = "any"
    ):
        """
        View the leaderboard.
        
        Args:
            interaction: The Discord interaction.
            metric: The metric to sort by.
            position: Filter by position.
        """
        # Get the registration cog to access player data
        registration_cog = self.bot.get_cog("RegistrationCog")
        if not registration_cog:
            await interaction.response.send_message(
                "Registration system is not available.",
                ephemeral=True
            )
            return
        
        # Check if there are any registered players
        if not registration_cog.players:
            await interaction.response.send_message(
                "No players are registered.",
                ephemeral=True
            )
            return
        
        # Convert position string to enum
        try:
            position_enum = Position.from_string(position)
        except ValueError:
            await interaction.response.send_message(
                f"Invalid position: {position}. Must be 'flank', 'pocket', or 'any'.",
                ephemeral=True
            )
            return
        
        # Filter players by minimum number of games
        min_games = 1
        players = [p for p in registration_cog.players.values() if p.games_played >= min_games]
        
        # Sort players by the specified metric
        if metric == "win_rate":
            if position_enum == Position.ANY:
                sorted_players = sorted(players, key=lambda p: p.get_win_rate(), reverse=True)
            else:
                sorted_players = sorted(
                    players,
                    key=lambda p: p.get_position_win_rate(position_enum),
                    reverse=True
                )
        elif metric == "games_played":
            if position_enum == Position.ANY:
                sorted_players = sorted(players, key=lambda p: p.games_played, reverse=True)
            else:
                sorted_players = sorted(
                    players,
                    key=lambda p: p.position_performance[position_enum]["games"],
                    reverse=True
                )
        elif metric == "games_won":
            if position_enum == Position.ANY:
                sorted_players = sorted(players, key=lambda p: p.games_won, reverse=True)
            else:
                sorted_players = sorted(
                    players,
                    key=lambda p: p.position_performance[position_enum]["wins"],
                    reverse=True
                )
        else:
            await interaction.response.send_message(
                f"Invalid metric: {metric}. Must be 'win_rate', 'games_played', or 'games_won'.",
                ephemeral=True
            )
            return
        
        # Create an embed with the leaderboard
        embed = discord.Embed(
            title=f"Leaderboard - {metric.replace('_', ' ').title()}",
            description=f"Position: {position_enum.value}",
            color=discord.Color.gold()
        )
        
        # Add players to the leaderboard
        for i, player in enumerate(sorted_players[:10]):
            if metric == "win_rate":
                if position_enum == Position.ANY:
                    value = f"{player.get_win_rate():.1f}% ({player.games_played} games)"
                else:
                    pos_games = player.position_performance[position_enum]["games"]
                    if pos_games > 0:
                        value = f"{player.get_position_win_rate(position_enum):.1f}% ({pos_games} games)"
                    else:
                        value = "N/A"
            elif metric == "games_played":
                if position_enum == Position.ANY:
                    value = str(player.games_played)
                else:
                    value = str(player.position_performance[position_enum]["games"])
            elif metric == "games_won":
                if position_enum == Position.ANY:
                    value = str(player.games_won)
                else:
                    value = str(player.position_performance[position_enum]["wins"])
            
            embed.add_field(
                name=f"{i+1}. {player.discord_name}",
                value=value,
                inline=False
            )
        
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    """
    Set up the stats cog.
    
    Args:
        bot: The Discord bot instance.
    """
    await bot.add_cog(StatsCog(bot)) 
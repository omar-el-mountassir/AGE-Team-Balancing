"""
Registration Cog for the Age of Empires 2 Team Balancing Bot.
Handles player registration and profile management.
"""

import discord
from discord import app_commands
from discord.ext import commands

import config
from src.api.api_factory import api_factory
from src.models.player import Player, Position
from src.utils.logger import get_logger

logger = get_logger(__name__)

class RegistrationCog(commands.Cog):
    """
    Cog for handling player registration and profile management.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the registration cog.
        
        Args:
            bot: The Discord bot instance.
        """
        self.bot = bot
        
        # In-memory storage for registered players (would be replaced with a database in production)
        self.players = {}  # Discord ID -> Player object
    
    @app_commands.command(name="register", description="Register yourself with your Steam nickname")
    @app_commands.describe(steam_nickname="Your Steam nickname")
    async def register(self, interaction: discord.Interaction, steam_nickname: str):
        """
        Register a player with their Steam nickname.
        
        Args:
            interaction: The Discord interaction.
            steam_nickname: The player's Steam nickname.
        """
        discord_id = interaction.user.id
        discord_name = interaction.user.name
        
        # Check if player is already registered
        if discord_id in self.players:
            await interaction.response.send_message(
                f"You are already registered as {self.players[discord_id].steam_nickname}. "
                f"Use `/update` to update your ELO ratings.",
                ephemeral=True
            )
            return
        
        # Create a new player
        player = Player(
            discord_id=discord_id,
            discord_name=discord_name,
            steam_nickname=steam_nickname
        )
        
        # Defer the response while we fetch ELO ratings
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        # Fetch ELO ratings from API
        try:
            elo_1v1, elo_team = await api_factory.get_player_elo(steam_nickname)
            
            if elo_1v1 is not None or elo_team is not None:
                player.update_elo(elo_1v1, elo_team)
                self.players[discord_id] = player
                
                await interaction.followup.send(
                    f"Successfully registered {steam_nickname}!\n"
                    f"1v1 ELO: {elo_1v1 or 'Not available'}\n"
                    f"Team ELO: {elo_team or 'Not available'}"
                )
            else:
                await interaction.followup.send(
                    f"Could not find ELO ratings for {steam_nickname}. "
                    f"You have been registered with no ELO ratings. "
                    f"You can update them later with `/update`."
                )
                self.players[discord_id] = player
        except Exception as e:
            logger.error(f"Error registering player {steam_nickname}: {e}")
            await interaction.followup.send(
                f"An error occurred while registering: {e}"
            )
    
    @app_commands.command(name="update", description="Update your ELO ratings")
    async def update(self, interaction: discord.Interaction):
        """
        Update a player's ELO ratings.
        
        Args:
            interaction: The Discord interaction.
        """
        discord_id = interaction.user.id
        
        # Check if player is registered
        if discord_id not in self.players:
            await interaction.response.send_message(
                "You are not registered. Use `/register` to register first.",
                ephemeral=True
            )
            return
        
        player = self.players[discord_id]
        
        # Defer the response while we fetch ELO ratings
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        # Fetch ELO ratings from API
        try:
            elo_1v1, elo_team = await api_factory.get_player_elo(player.steam_nickname)
            
            if elo_1v1 is not None or elo_team is not None:
                player.update_elo(elo_1v1, elo_team)
                
                await interaction.followup.send(
                    f"Successfully updated ELO ratings for {player.steam_nickname}!\n"
                    f"1v1 ELO: {elo_1v1 or 'Not available'}\n"
                    f"Team ELO: {elo_team or 'Not available'}"
                )
            else:
                await interaction.followup.send(
                    f"Could not find ELO ratings for {player.steam_nickname}."
                )
        except Exception as e:
            logger.error(f"Error updating ELO ratings for {player.steam_nickname}: {e}")
            await interaction.followup.send(
                f"An error occurred while updating ELO ratings: {e}"
            )
    
    @app_commands.command(name="profile", description="View your profile or another player's profile")
    @app_commands.describe(user="The user to view the profile of (leave empty for your own profile)")
    async def profile(self, interaction: discord.Interaction, user: discord.User = None):
        """
        View a player's profile.
        
        Args:
            interaction: The Discord interaction.
            user: The user to view the profile of. If None, view the caller's profile.
        """
        target_user = user or interaction.user
        discord_id = target_user.id
        
        # Check if player is registered
        if discord_id not in self.players:
            await interaction.response.send_message(
                f"{target_user.name} is not registered.",
                ephemeral=True
            )
            return
        
        player = self.players[discord_id]
        
        # Create an embed with player information
        embed = discord.Embed(
            title=f"Profile: {player.discord_name}",
            color=discord.Color.blue()
        )
        
        embed.add_field(name="Steam Nickname", value=player.steam_nickname, inline=False)
        embed.add_field(name="1v1 ELO", value=player.elo_1v1 or "Not available", inline=True)
        embed.add_field(name="Team ELO", value=player.elo_team or "Not available", inline=True)
        embed.add_field(name="Preferred Position", value=player.preferred_position.value, inline=True)
        
        if player.preferred_civs:
            embed.add_field(name="Preferred Civilizations", value=", ".join(player.preferred_civs), inline=False)
        
        embed.add_field(name="Games Played", value=player.games_played, inline=True)
        embed.add_field(name="Win Rate", value=f"{player.get_win_rate():.1f}%", inline=True)
        
        # Add position-specific stats if available
        flank_games = player.position_performance[Position.FLANK]["games"]
        pocket_games = player.position_performance[Position.POCKET]["games"]
        
        if flank_games > 0:
            flank_win_rate = player.get_position_win_rate(Position.FLANK)
            embed.add_field(name="Flank Stats", value=f"{flank_games} games, {flank_win_rate:.1f}% win rate", inline=True)
        
        if pocket_games > 0:
            pocket_win_rate = player.get_position_win_rate(Position.POCKET)
            embed.add_field(name="Pocket Stats", value=f"{pocket_games} games, {pocket_win_rate:.1f}% win rate", inline=True)
        
        # Add tags if available
        if player.tags:
            embed.add_field(name="Tags", value=", ".join(player.tags), inline=False)
        
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="preferences", description="Set your position and civilization preferences")
    @app_commands.describe(
        position="Your preferred position (flank, pocket, or any)",
        civilizations="Comma-separated list of your preferred civilizations"
    )
    async def preferences(
        self, 
        interaction: discord.Interaction, 
        position: str,
        civilizations: str = None
    ):
        """
        Set a player's preferences.
        
        Args:
            interaction: The Discord interaction.
            position: The preferred position.
            civilizations: Comma-separated list of preferred civilizations.
        """
        discord_id = interaction.user.id
        
        # Check if player is registered
        if discord_id not in self.players:
            await interaction.response.send_message(
                "You are not registered. Use `/register` to register first.",
                ephemeral=True
            )
            return
        
        player = self.players[discord_id]
        
        # Update position preference
        try:
            position_enum = Position.from_string(position)
            player.set_preferred_position(position_enum)
        except ValueError:
            await interaction.response.send_message(
                f"Invalid position: {position}. Must be 'flank', 'pocket', or 'any'.",
                ephemeral=True
            )
            return
        
        # Update civilization preferences if provided
        if civilizations:
            # Clear existing preferences
            player.preferred_civs.clear()
            
            # Add new preferences
            for civ in civilizations.split(","):
                civ = civ.strip()
                if civ:
                    player.add_preferred_civ(civ)
        
        await interaction.response.send_message(
            f"Preferences updated!\n"
            f"Position: {player.preferred_position.value}\n"
            f"Civilizations: {', '.join(player.preferred_civs) if player.preferred_civs else 'None'}"
        )

async def setup(bot: commands.Bot):
    """
    Set up the registration cog.
    
    Args:
        bot: The Discord bot instance.
    """
    await bot.add_cog(RegistrationCog(bot)) 
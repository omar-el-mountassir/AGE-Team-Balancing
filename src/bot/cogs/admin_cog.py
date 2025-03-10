"""
Admin Cog for the Age of Empires 2 Team Balancing Bot.
Provides administrative commands for managing the bot.
"""

import discord
from discord import app_commands
from discord.ext import commands

import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AdminCog(commands.Cog):
    """
    Cog for administrative commands.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the admin cog.
        
        Args:
            bot: The Discord bot instance.
        """
        self.bot = bot
    
    @app_commands.command(name="admin_update_elo", description="Force update of a player's ELO ratings")
    @app_commands.describe(user="The user to update ELO ratings for")
    @app_commands.default_permissions(administrator=True)
    async def admin_update_elo(self, interaction: discord.Interaction, user: discord.User):
        """
        Force update of a player's ELO ratings.
        
        Args:
            interaction: The Discord interaction.
            user: The user to update ELO ratings for.
        """
        # Get the registration cog to access player data
        registration_cog = self.bot.get_cog("RegistrationCog")
        if not registration_cog:
            await interaction.response.send_message(
                "Registration system is not available.",
                ephemeral=True
            )
            return
        
        discord_id = user.id
        
        # Check if player is registered
        if discord_id not in registration_cog.players:
            await interaction.response.send_message(
                f"{user.name} is not registered.",
                ephemeral=True
            )
            return
        
        player = registration_cog.players[discord_id]
        
        # Defer the response while we fetch ELO ratings
        await interaction.response.defer(ephemeral=True, thinking=True)
        
        # Fetch ELO ratings from API
        try:
            from src.api.api_factory import api_factory
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
    
    @app_commands.command(name="admin_force", description="Force a player into a specific team")
    @app_commands.describe(
        user="The user to force into a team",
        team="The team number to force the user into"
    )
    @app_commands.default_permissions(administrator=True)
    async def admin_force(self, interaction: discord.Interaction, user: discord.User, team: int):
        """
        Force a player into a specific team.
        
        Args:
            interaction: The Discord interaction.
            user: The user to force into a team.
            team: The team number to force the user into.
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
        
        # Check if the team number is valid
        if team < 1 or team > len(composition):
            await interaction.response.send_message(
                f"Invalid team number. Must be between 1 and {len(composition)}.",
                ephemeral=True
            )
            return
        
        # Find the player in the teams
        player_found = False
        player_team = None
        player_member = None
        
        for i, t in enumerate(composition):
            for member in t.members:
                if member.player.discord_id == user.id:
                    player_found = True
                    player_team = i
                    player_member = member
                    break
            if player_found:
                break
        
        if not player_found:
            await interaction.response.send_message(
                f"{user.name} is not in any team in the current composition.",
                ephemeral=True
            )
            return
        
        # If the player is already in the target team, do nothing
        if player_team == team - 1:
            await interaction.response.send_message(
                f"{user.name} is already in Team {team}.",
                ephemeral=True
            )
            return
        
        # Move the player to the target team
        # First, remove from current team
        composition[player_team].remove_member(user.id)
        
        # Then, add to target team
        composition[team - 1].add_member(
            player_member.player,
            player_member.position,
            player_member.civilization
        )
        
        await interaction.response.send_message(
            f"Moved {user.name} from Team {player_team + 1} to Team {team}.",
            ephemeral=False
        )
    
    @app_commands.command(name="admin_config", description="View or modify bot configuration")
    @app_commands.describe(
        setting="The configuration setting to view or modify",
        value="The new value for the setting (leave empty to view current value)"
    )
    @app_commands.default_permissions(administrator=True)
    async def admin_config(
        self, 
        interaction: discord.Interaction, 
        setting: str,
        value: str = None
    ):
        """
        View or modify bot configuration.
        
        Args:
            interaction: The Discord interaction.
            setting: The configuration setting to view or modify.
            value: The new value for the setting (leave empty to view current value).
        """
        # Get all configuration
        all_config = config.get_all_config()
        
        # Check if the setting exists
        if setting.upper() not in all_config:
            await interaction.response.send_message(
                f"Unknown configuration setting: {setting}",
                ephemeral=True
            )
            return
        
        # If no value is provided, just show the current value
        if value is None:
            await interaction.response.send_message(
                f"Current value of {setting.upper()}: {all_config[setting.upper()]}",
                ephemeral=True
            )
            return
        
        # Modifying configuration at runtime is not implemented yet
        await interaction.response.send_message(
            "Modifying configuration at runtime is not implemented yet. "
            "Please modify the .env file and restart the bot.",
            ephemeral=True
        )
    
    @app_commands.command(name="admin_status", description="View bot status")
    @app_commands.default_permissions(administrator=True)
    async def admin_status(self, interaction: discord.Interaction):
        """
        View bot status.
        
        Args:
            interaction: The Discord interaction.
        """
        # Create an embed with bot status information
        embed = discord.Embed(
            title="Bot Status",
            color=discord.Color.blue()
        )
        
        # Add basic bot information
        embed.add_field(name="Bot Name", value=self.bot.user.name, inline=True)
        embed.add_field(name="Bot ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Uptime", value=f"{(discord.utils.utcnow() - self.bot.start_time).total_seconds() / 60:.1f} minutes", inline=True)
        
        # Add server information
        embed.add_field(name="Servers", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Users", value=sum(guild.member_count for guild in self.bot.guilds), inline=True)
        
        # Add queue information
        balancing_cog = self.bot.get_cog("BalancingCog")
        if balancing_cog:
            embed.add_field(name="Queue Size", value=len(balancing_cog.queue), inline=True)
        
        # Add player information
        registration_cog = self.bot.get_cog("RegistrationCog")
        if registration_cog:
            embed.add_field(name="Registered Players", value=len(registration_cog.players), inline=True)
        
        # Add configuration information
        all_config = config.get_all_config()
        config_text = "\n".join(f"{key}: {value}" for key, value in all_config.items())
        embed.add_field(name="Configuration", value=f"```{config_text}```", inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    """
    Set up the admin cog.
    
    Args:
        bot: The Discord bot instance.
    """
    await bot.add_cog(AdminCog(bot)) 
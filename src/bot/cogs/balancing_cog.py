"""
Balancing Cog for the Age of Empires 2 Team Balancing Bot.
Handles team balancing and queue management.
"""

import asyncio
from typing import Dict, List, Optional, Set

import discord
from discord import app_commands
from discord.ext import commands

import config
from src.balancer.team_balancer import TeamBalancer
from src.models.player import Player, Position
from src.models.team import Team
from src.utils.logger import get_logger

logger = get_logger(__name__)

class BalancingCog(commands.Cog):
    """
    Cog for handling team balancing and queue management.
    """
    
    def __init__(self, bot: commands.Bot):
        """
        Initialize the balancing cog.
        
        Args:
            bot: The Discord bot instance.
        """
        self.bot = bot
        self.team_balancer = TeamBalancer()
        
        # Queue of players waiting for a game
        self.queue = []  # List of Player objects
        
        # Current team compositions
        self.current_compositions = []  # List of List[Team]
        
        # Lock for queue operations
        self.queue_lock = asyncio.Lock()
    
    @app_commands.command(name="queue", description="Join the queue for a game")
    @app_commands.describe(position="Your preferred position for this game (flank, pocket, or any)")
    async def queue_command(self, interaction: discord.Interaction, position: Optional[str] = None):
        """
        Join the queue for a game.
        
        Args:
            interaction: The Discord interaction.
            position: The preferred position for this game.
        """
        # Get the registration cog to access player data
        registration_cog = self.bot.get_cog("RegistrationCog")
        if not registration_cog:
            await interaction.response.send_message(
                "Registration system is not available.",
                ephemeral=True
            )
            return
        
        discord_id = interaction.user.id
        
        # Check if player is registered
        if discord_id not in registration_cog.players:
            await interaction.response.send_message(
                "You are not registered. Use `/register` to register first.",
                ephemeral=True
            )
            return
        
        player = registration_cog.players[discord_id]
        
        # Update position preference for this game if provided
        if position:
            try:
                temp_position = Position.from_string(position)
                # This is a temporary preference just for this game
                # We don't update the player's stored preference
                player.preferred_position = temp_position
            except ValueError:
                await interaction.response.send_message(
                    f"Invalid position: {position}. Must be 'flank', 'pocket', or 'any'.",
                    ephemeral=True
                )
                return
        
        async with self.queue_lock:
            # Check if player is already in queue
            if any(p.discord_id == discord_id for p in self.queue):
                await interaction.response.send_message(
                    "You are already in the queue.",
                    ephemeral=True
                )
                return
            
            # Add player to queue
            self.queue.append(player)
            
            await interaction.response.send_message(
                f"You have joined the queue! Current queue size: {len(self.queue)}",
                ephemeral=False
            )
    
    @app_commands.command(name="leave", description="Leave the queue")
    async def leave(self, interaction: discord.Interaction):
        """
        Leave the queue.
        
        Args:
            interaction: The Discord interaction.
        """
        discord_id = interaction.user.id
        
        async with self.queue_lock:
            # Check if player is in queue
            for i, player in enumerate(self.queue):
                if player.discord_id == discord_id:
                    self.queue.pop(i)
                    await interaction.response.send_message(
                        f"You have left the queue. Current queue size: {len(self.queue)}",
                        ephemeral=False
                    )
                    return
            
            await interaction.response.send_message(
                "You are not in the queue.",
                ephemeral=True
            )
    
    @app_commands.command(name="status", description="Check the current queue status")
    async def status(self, interaction: discord.Interaction):
        """
        Check the current queue status.
        
        Args:
            interaction: The Discord interaction.
        """
        async with self.queue_lock:
            if not self.queue:
                await interaction.response.send_message(
                    "The queue is empty.",
                    ephemeral=False
                )
                return
            
            # Create an embed with queue information
            embed = discord.Embed(
                title="Queue Status",
                description=f"There are {len(self.queue)} players in the queue.",
                color=discord.Color.blue()
            )
            
            # Add players to the embed
            for i, player in enumerate(self.queue):
                embed.add_field(
                    name=f"{i+1}. {player.discord_name}",
                    value=f"Position: {player.preferred_position.value}\n"
                          f"1v1 ELO: {player.elo_1v1 or 'N/A'}\n"
                          f"Team ELO: {player.elo_team or 'N/A'}",
                    inline=True
                )
            
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="balance", description="Generate balanced team compositions")
    @app_commands.describe(
        team_size="The number of players per team (e.g., 2 for 2v2, 3 for 3v3, etc.)",
        respect_preferences="Whether to respect position preferences (default: True)"
    )
    async def balance(
        self, 
        interaction: discord.Interaction, 
        team_size: int,
        respect_preferences: bool = True
    ):
        """
        Generate balanced team compositions.
        
        Args:
            interaction: The Discord interaction.
            team_size: The number of players per team.
            respect_preferences: Whether to respect position preferences.
        """
        async with self.queue_lock:
            # Check if there are enough players
            if len(self.queue) < team_size * 2:
                await interaction.response.send_message(
                    f"Not enough players in the queue. Need {team_size * 2}, have {len(self.queue)}.",
                    ephemeral=True
                )
                return
            
            # Check if the number of players is divisible by the team size
            if len(self.queue) % team_size != 0:
                await interaction.response.send_message(
                    f"The number of players ({len(self.queue)}) must be divisible by the team size ({team_size}).",
                    ephemeral=True
                )
                return
            
            # Defer the response while we generate team compositions
            await interaction.response.defer(thinking=True)
            
            try:
                # Generate team compositions
                self.current_compositions = self.team_balancer.generate_team_compositions(
                    players=self.queue,
                    team_size=team_size,
                    num_compositions=3,
                    respect_preferences=respect_preferences
                )
                
                # Create embeds for each composition
                embeds = []
                
                for i, composition in enumerate(self.current_compositions):
                    embed = discord.Embed(
                        title=f"Team Composition {i+1}",
                        description=f"{team_size}v{team_size} Balanced Teams",
                        color=discord.Color.blue()
                    )
                    
                    # Calculate team scores
                    team_scores = [self.team_balancer.calculate_team_score(team) for team in composition]
                    score_diff = max(team_scores) - min(team_scores)
                    score_diff_percent = (score_diff / sum(team_scores)) * 100
                    
                    embed.add_field(
                        name="Balance",
                        value=f"Score Difference: {score_diff:.1f} ({score_diff_percent:.1f}%)",
                        inline=False
                    )
                    
                    # Add teams to the embed
                    for j, team in enumerate(composition):
                        team_text = ""
                        
                        for member in team.members:
                            player = member.player
                            team_text += f"**{player.discord_name}** ({player.elo_1v1 or 'N/A'}/{player.elo_team or 'N/A'}) - {member.position.value}\n"
                        
                        embed.add_field(
                            name=f"Team {j+1} (Score: {team_scores[j]:.1f})",
                            value=team_text,
                            inline=True
                        )
                    
                    embeds.append(embed)
                
                # Send the embeds
                for embed in embeds:
                    await interaction.followup.send(embed=embed)
                
                # Add buttons to select a composition
                view = TeamSelectionView(self)
                await interaction.followup.send(
                    "Select a team composition to use:",
                    view=view
                )
            except Exception as e:
                logger.error(f"Error generating team compositions: {e}")
                await interaction.followup.send(
                    f"An error occurred while generating team compositions: {e}"
                )
    
    @app_commands.command(name="clear_queue", description="Clear the queue")
    @app_commands.default_permissions(administrator=True)
    async def clear_queue(self, interaction: discord.Interaction):
        """
        Clear the queue.
        
        Args:
            interaction: The Discord interaction.
        """
        async with self.queue_lock:
            self.queue.clear()
            self.current_compositions.clear()
            
            await interaction.response.send_message(
                "Queue cleared.",
                ephemeral=False
            )

class TeamSelectionView(discord.ui.View):
    """
    View for selecting a team composition.
    """
    
    def __init__(self, cog: BalancingCog):
        """
        Initialize the team selection view.
        
        Args:
            cog: The balancing cog.
        """
        super().__init__(timeout=300)  # 5 minute timeout
        self.cog = cog
    
    @discord.ui.button(label="Composition 1", style=discord.ButtonStyle.primary)
    async def composition_1(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Select composition 1.
        
        Args:
            interaction: The Discord interaction.
            button: The button that was clicked.
        """
        await self.select_composition(interaction, 0)
    
    @discord.ui.button(label="Composition 2", style=discord.ButtonStyle.primary)
    async def composition_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Select composition 2.
        
        Args:
            interaction: The Discord interaction.
            button: The button that was clicked.
        """
        await self.select_composition(interaction, 1)
    
    @discord.ui.button(label="Composition 3", style=discord.ButtonStyle.primary)
    async def composition_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        Select composition 3.
        
        Args:
            interaction: The Discord interaction.
            button: The button that was clicked.
        """
        await self.select_composition(interaction, 2)
    
    async def select_composition(self, interaction: discord.Interaction, index: int):
        """
        Select a composition.
        
        Args:
            interaction: The Discord interaction.
            index: The index of the composition to select.
        """
        if index >= len(self.cog.current_compositions):
            await interaction.response.send_message(
                "Invalid composition index.",
                ephemeral=True
            )
            return
        
        composition = self.cog.current_compositions[index]
        
        # Create a message mentioning all players
        mentions = []
        for team in composition:
            for member in team.members:
                mentions.append(f"<@{member.player.discord_id}>")
        
        # Disable all buttons
        for item in self.children:
            item.disabled = True
        
        await interaction.response.edit_message(view=self)
        
        # Send a message with the selected composition
        await interaction.followup.send(
            f"Composition {index+1} selected!\n\n"
            f"Players: {' '.join(mentions)}\n\n"
            f"Please join the appropriate voice channels for your teams."
        )
        
        # Clear the queue
        async with self.cog.queue_lock:
            self.cog.queue.clear()
    
    async def on_timeout(self):
        """Handle the view timing out."""
        # Disable all buttons
        for item in self.children:
            item.disabled = True
        
        # We can't edit the message here because we don't have the interaction
        # The buttons will just stop working after the timeout

async def setup(bot: commands.Bot):
    """
    Set up the balancing cog.
    
    Args:
        bot: The Discord bot instance.
    """
    await bot.add_cog(BalancingCog(bot)) 
"""
Main entry point for the Age of Empires 2 Team Balancing Bot.
This script initializes the bot, sets up logging, and starts the bot.
"""

import asyncio
import logging
import sys
from typing import Optional

import discord
from discord.ext import commands

import config
from src.utils.logger import setup_logger

# Set up logging
logger = setup_logger(__name__)

class AGETeamBalancer(commands.Bot):
    """
    Main bot class for Age of Empires 2 Team Balancing.
    """
    
    def __init__(self) -> None:
        """Initialize the bot with intents and command prefix."""
        # Set up intents - we need members intent to access the members in the server
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        
        super().__init__(
            command_prefix=config.COMMAND_PREFIX,
            intents=intents,
            activity=discord.Game(name=config.BOT_STATUS),
            help_command=None  # We'll implement our own help command
        )
        
        # Store initialization timestamp
        self.start_time = discord.utils.utcnow()
        
    async def setup_hook(self) -> None:
        """
        This is called when the bot is starting up.
        Load all cogs and perform initialization tasks.
        """
        logger.info("Bot is starting up...")
        
        # List of cogs to load
        initial_cogs = [
            'src.bot.cogs.registration_cog',
            'src.bot.cogs.balancing_cog',
            'src.bot.cogs.admin_cog',
            'src.bot.cogs.stats_cog',
        ]
        
        # Load all cogs
        for cog in initial_cogs:
            try:
                await self.load_extension(cog)
                logger.info(f"Loaded extension: {cog}")
            except Exception as e:
                logger.error(f"Failed to load extension {cog}: {e}")
                
        logger.info("Bot setup completed")
        
    async def on_ready(self) -> None:
        """Called when the bot is ready and connected to Discord."""
        logger.info(f"Logged in as {self.user.name} (ID: {self.user.id})")
        logger.info(f"Connected to {len(self.guilds)} guilds:")
        
        for guild in self.guilds:
            logger.info(f"- {guild.name} (ID: {guild.id})")
            
        logger.info(f"Bot is ready with prefix: {config.COMMAND_PREFIX}")
        
    async def on_command_error(self, ctx: commands.Context, error: Exception) -> None:
        """Global error handler for command errors."""
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore command not found errors
            
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
            return
            
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"Bad argument: {error}")
            return
            
        # Log all other errors
        logger.error(f"Command error in {ctx.command}: {error}")
        await ctx.send(f"An error occurred: {error}")

async def main() -> None:
    """Main function to start the bot."""
    # Initialize the bot
    bot = AGETeamBalancer()
    
    # Start the bot with the token from config
    if not config.DISCORD_TOKEN:
        logger.critical("No Discord token provided. Please set the DISCORD_TOKEN environment variable.")
        sys.exit(1)
        
    try:
        logger.info("Starting bot...")
        await bot.start(config.DISCORD_TOKEN)
    except discord.LoginFailure:
        logger.critical("Invalid Discord token. Please check your DISCORD_TOKEN environment variable.")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"An error occurred while starting the bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Run the bot in an asyncio event loop
    asyncio.run(main()) 
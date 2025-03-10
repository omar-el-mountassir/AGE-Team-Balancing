"""
API Factory for the Age of Empires 2 Team Balancing Bot.
Manages multiple API clients and provides fallback mechanisms.
"""

import asyncio
from typing import Dict, List, Optional, Tuple, Union

import config
from src.api.api_client_interface import APIClientInterface
from src.api.aoe2gg_client import AoE2GGClient
from src.utils.logger import get_logger

logger = get_logger(__name__)

class APIFactory:
    """
    Factory class for managing multiple API clients.
    Provides fallback mechanisms if one API is unavailable.
    """
    
    def __init__(self):
        """Initialize the API factory."""
        self.clients = []
        self.available_clients = []
        self.initialized = False
    
    async def initialize(self):
        """Initialize all API clients and check their availability."""
        if self.initialized:
            return
        
        # Create API clients
        self.clients = [
            AoE2GGClient(),
            # Add other API clients here as they are implemented
            # AoENexusClient(),
            # AoCRecClient(),
        ]
        
        # Check which clients are available
        availability_tasks = [client.is_available() for client in self.clients]
        availability_results = await asyncio.gather(*availability_tasks, return_exceptions=True)
        
        self.available_clients = []
        for i, result in enumerate(availability_results):
            client = self.clients[i]
            if isinstance(result, Exception):
                logger.warning(f"Error checking availability of {client.get_name()}: {result}")
            elif result:
                logger.info(f"API client {client.get_name()} is available")
                self.available_clients.append(client)
            else:
                logger.warning(f"API client {client.get_name()} is not available")
        
        if not self.available_clients:
            logger.error("No API clients are available")
        
        self.initialized = True
    
    async def get_player_elo(self, steam_id: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Get a player's ELO ratings using available API clients.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            
        Returns:
            A tuple containing (1v1_elo, team_elo), or (None, None) if not found.
        """
        await self.initialize()
        
        for client in self.available_clients:
            try:
                elo_1v1, elo_team = await client.get_player_elo(steam_id)
                if elo_1v1 is not None or elo_team is not None:
                    logger.info(f"Got ELO ratings from {client.get_name()}")
                    return elo_1v1, elo_team
            except Exception as e:
                logger.error(f"Error getting ELO ratings from {client.get_name()}: {e}")
        
        logger.warning(f"Could not get ELO ratings for {steam_id} from any API")
        return None, None
    
    async def get_player_match_history(self, steam_id: str, limit: int = 10) -> List[Dict]:
        """
        Get a player's match history using available API clients.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            limit: The maximum number of matches to return.
            
        Returns:
            A list of match data dictionaries.
        """
        await self.initialize()
        
        for client in self.available_clients:
            try:
                matches = await client.get_player_match_history(steam_id, limit)
                if matches:
                    logger.info(f"Got match history from {client.get_name()}")
                    return matches
            except Exception as e:
                logger.error(f"Error getting match history from {client.get_name()}: {e}")
        
        logger.warning(f"Could not get match history for {steam_id} from any API")
        return []
    
    async def get_player_civilization_stats(self, steam_id: str) -> Dict[str, Dict]:
        """
        Get a player's statistics for each civilization using available API clients.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            
        Returns:
            A dictionary mapping civilization names to statistics.
        """
        await self.initialize()
        
        for client in self.available_clients:
            try:
                stats = await client.get_player_civilization_stats(steam_id)
                if stats:
                    logger.info(f"Got civilization stats from {client.get_name()}")
                    return stats
            except Exception as e:
                logger.error(f"Error getting civilization stats from {client.get_name()}: {e}")
        
        logger.warning(f"Could not get civilization stats for {steam_id} from any API")
        return {}
    
    async def search_player(self, query: str) -> List[Dict]:
        """
        Search for players by name using available API clients.
        
        Args:
            query: The search query.
            
        Returns:
            A list of player data dictionaries.
        """
        await self.initialize()
        
        for client in self.available_clients:
            try:
                players = await client.search_player(query)
                if players:
                    logger.info(f"Got player search results from {client.get_name()}")
                    return players
            except Exception as e:
                logger.error(f"Error searching players from {client.get_name()}: {e}")
        
        logger.warning(f"Could not search players for '{query}' from any API")
        return []
    
    async def get_civilization_data(self, civilization: str) -> Optional[Dict]:
        """
        Get data for a specific civilization using available API clients.
        
        Args:
            civilization: The name of the civilization.
            
        Returns:
            A dictionary containing civilization data, or None if not found.
        """
        await self.initialize()
        
        for client in self.available_clients:
            try:
                data = await client.get_civilization_data(civilization)
                if data:
                    logger.info(f"Got civilization data from {client.get_name()}")
                    return data
            except Exception as e:
                logger.error(f"Error getting civilization data from {client.get_name()}: {e}")
        
        logger.warning(f"Could not get data for civilization '{civilization}' from any API")
        return None
    
    async def get_current_meta(self) -> Dict[str, Dict]:
        """
        Get the current meta data using available API clients.
        
        Returns:
            A dictionary containing meta data.
        """
        await self.initialize()
        
        for client in self.available_clients:
            try:
                meta = await client.get_current_meta()
                if meta:
                    logger.info(f"Got meta data from {client.get_name()}")
                    return meta
            except Exception as e:
                logger.error(f"Error getting meta data from {client.get_name()}: {e}")
        
        logger.warning("Could not get meta data from any API")
        return {}
    
    async def get_map_data(self, map_name: str) -> Optional[Dict]:
        """
        Get data for a specific map using available API clients.
        
        Args:
            map_name: The name of the map.
            
        Returns:
            A dictionary containing map data, or None if not found.
        """
        await self.initialize()
        
        for client in self.available_clients:
            try:
                data = await client.get_map_data(map_name)
                if data:
                    logger.info(f"Got map data from {client.get_name()}")
                    return data
            except Exception as e:
                logger.error(f"Error getting map data from {client.get_name()}: {e}")
        
        logger.warning(f"Could not get data for map '{map_name}' from any API")
        return None
    
    async def close(self):
        """Close all API clients."""
        for client in self.clients:
            try:
                if hasattr(client, 'close') and callable(client.close):
                    await client.close()
            except Exception as e:
                logger.error(f"Error closing API client {client.get_name()}: {e}")

# Singleton instance
api_factory = APIFactory() 
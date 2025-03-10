"""
API Client Interface for the Age of Empires 2 Team Balancing Bot.
Defines the interface that all API clients must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple, Union

class APIClientInterface(ABC):
    """
    Interface for API clients that fetch player data.
    All API clients should implement this interface.
    """
    
    @abstractmethod
    async def get_player_elo(self, steam_id: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Get a player's ELO ratings.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            
        Returns:
            A tuple containing (1v1_elo, team_elo), or (None, None) if not found.
        """
        pass
    
    @abstractmethod
    async def get_player_match_history(self, steam_id: str, limit: int = 10) -> List[Dict]:
        """
        Get a player's match history.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            limit: The maximum number of matches to return.
            
        Returns:
            A list of match data dictionaries.
        """
        pass
    
    @abstractmethod
    async def get_player_civilization_stats(self, steam_id: str) -> Dict[str, Dict]:
        """
        Get a player's statistics for each civilization.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            
        Returns:
            A dictionary mapping civilization names to statistics.
        """
        pass
    
    @abstractmethod
    async def search_player(self, query: str) -> List[Dict]:
        """
        Search for players by name.
        
        Args:
            query: The search query.
            
        Returns:
            A list of player data dictionaries.
        """
        pass
    
    @abstractmethod
    async def get_civilization_data(self, civilization: str) -> Optional[Dict]:
        """
        Get data for a specific civilization.
        
        Args:
            civilization: The name of the civilization.
            
        Returns:
            A dictionary containing civilization data, or None if not found.
        """
        pass
    
    @abstractmethod
    async def get_current_meta(self) -> Dict[str, Dict]:
        """
        Get the current meta data, including civilization tiers.
        
        Returns:
            A dictionary containing meta data.
        """
        pass
    
    @abstractmethod
    async def get_map_data(self, map_name: str) -> Optional[Dict]:
        """
        Get data for a specific map.
        
        Args:
            map_name: The name of the map.
            
        Returns:
            A dictionary containing map data, or None if not found.
        """
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """
        Check if the API is available.
        
        Returns:
            True if the API is available, False otherwise.
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the API.
        
        Returns:
            The name of the API.
        """
        pass 
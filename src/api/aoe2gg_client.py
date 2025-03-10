"""
AoE2.GG API Client for the Age of Empires 2 Team Balancing Bot.
Implements the API client interface for the AoE2.GG API.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Union

import aiohttp
from cachetools import TTLCache

import config
from src.api.api_client_interface import APIClientInterface
from src.utils.logger import get_logger

logger = get_logger(__name__)

class AoE2GGClient(APIClientInterface):
    """
    API client for the AoE2.GG API.
    """
    
    def __init__(self):
        """Initialize the API client."""
        self.base_url = config.AOE2_GG_API_BASE_URL
        self.timeout = config.API_TIMEOUT
        self.session = None
        
        # Cache for API responses
        self.cache = TTLCache(maxsize=1000, ttl=config.API_CACHE_TTL)
        
        # Rate limiting
        self.request_semaphore = asyncio.Semaphore(5)  # Max 5 concurrent requests
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Minimum time between requests in seconds
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create an aiohttp session.
        
        Returns:
            An aiohttp ClientSession.
        """
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.timeout)
            )
        return self.session
    
    async def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make a request to the API.
        
        Args:
            endpoint: The API endpoint to request.
            params: Query parameters to include in the request.
            
        Returns:
            The JSON response as a dictionary, or None if the request failed.
        """
        # Check cache first
        cache_key = f"{endpoint}:{str(params)}"
        if cache_key in self.cache:
            logger.debug(f"Cache hit for {cache_key}")
            return self.cache[cache_key]
        
        # Rate limiting
        async with self.request_semaphore:
            # Ensure minimum time between requests
            current_time = asyncio.get_event_loop().time()
            time_since_last_request = current_time - self.last_request_time
            if time_since_last_request < self.min_request_interval:
                await asyncio.sleep(self.min_request_interval - time_since_last_request)
            
            self.last_request_time = asyncio.get_event_loop().time()
            
            # Make the request
            try:
                session = await self._get_session()
                url = f"{self.base_url}/{endpoint}"
                
                logger.debug(f"Making request to {url} with params {params}")
                
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        # Cache the response
                        self.cache[cache_key] = data
                        return data
                    else:
                        logger.warning(f"API request failed: {response.status} - {await response.text()}")
                        return None
            except aiohttp.ClientError as e:
                logger.error(f"API request error: {e}")
                return None
            except asyncio.TimeoutError:
                logger.error(f"API request timeout for {endpoint}")
                return None
            except Exception as e:
                logger.error(f"Unexpected error in API request: {e}")
                return None
    
    async def get_player_elo(self, steam_id: str) -> Tuple[Optional[int], Optional[int]]:
        """
        Get a player's ELO ratings.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            
        Returns:
            A tuple containing (1v1_elo, team_elo), or (None, None) if not found.
        """
        data = await self._make_request(f"players/{steam_id}/ratings")
        
        if not data or "ratings" not in data:
            return None, None
        
        ratings = data["ratings"]
        elo_1v1 = None
        elo_team = None
        
        for rating in ratings:
            if rating.get("leaderboard_id") == 3:  # 1v1 Random Map
                elo_1v1 = rating.get("rating")
            elif rating.get("leaderboard_id") == 4:  # Team Random Map
                elo_team = rating.get("rating")
        
        return elo_1v1, elo_team
    
    async def get_player_match_history(self, steam_id: str, limit: int = 10) -> List[Dict]:
        """
        Get a player's match history.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            limit: The maximum number of matches to return.
            
        Returns:
            A list of match data dictionaries.
        """
        data = await self._make_request(f"players/{steam_id}/matches", {"count": limit})
        
        if not data or "matches" not in data:
            return []
        
        return data["matches"]
    
    async def get_player_civilization_stats(self, steam_id: str) -> Dict[str, Dict]:
        """
        Get a player's statistics for each civilization.
        
        Args:
            steam_id: The player's Steam ID or nickname.
            
        Returns:
            A dictionary mapping civilization names to statistics.
        """
        data = await self._make_request(f"players/{steam_id}/civilizations")
        
        if not data or "civilizations" not in data:
            return {}
        
        # Convert to a more usable format
        result = {}
        for civ_data in data["civilizations"]:
            civ_name = civ_data.get("name", "Unknown")
            result[civ_name] = {
                "games": civ_data.get("games_count", 0),
                "wins": civ_data.get("wins_count", 0),
                "win_rate": civ_data.get("win_rate", 0),
            }
        
        return result
    
    async def search_player(self, query: str) -> List[Dict]:
        """
        Search for players by name.
        
        Args:
            query: The search query.
            
        Returns:
            A list of player data dictionaries.
        """
        data = await self._make_request("players/search", {"query": query})
        
        if not data or "players" not in data:
            return []
        
        return data["players"]
    
    async def get_civilization_data(self, civilization: str) -> Optional[Dict]:
        """
        Get data for a specific civilization.
        
        Args:
            civilization: The name of the civilization.
            
        Returns:
            A dictionary containing civilization data, or None if not found.
        """
        # AoE2.GG doesn't have a specific endpoint for civilization data
        # This would typically be implemented with local data
        return None
    
    async def get_current_meta(self) -> Dict[str, Dict]:
        """
        Get the current meta data, including civilization tiers.
        
        Returns:
            A dictionary containing meta data.
        """
        # AoE2.GG doesn't have a specific endpoint for meta data
        # This would typically be implemented with local data
        return {}
    
    async def get_map_data(self, map_name: str) -> Optional[Dict]:
        """
        Get data for a specific map.
        
        Args:
            map_name: The name of the map.
            
        Returns:
            A dictionary containing map data, or None if not found.
        """
        # AoE2.GG doesn't have a specific endpoint for map data
        # This would typically be implemented with local data
        return None
    
    async def is_available(self) -> bool:
        """
        Check if the API is available.
        
        Returns:
            True if the API is available, False otherwise.
        """
        try:
            # Make a simple request to check if the API is available
            session = await self._get_session()
            url = f"{self.base_url}/leaderboards"
            
            async with session.get(url) as response:
                return response.status == 200
        except Exception:
            return False
    
    def get_name(self) -> str:
        """
        Get the name of the API.
        
        Returns:
            The name of the API.
        """
        return "AoE2.GG"
    
    async def close(self):
        """Close the aiohttp session."""
        if self.session and not self.session.closed:
            await self.session.close() 
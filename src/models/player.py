"""
Player model for the Age of Empires 2 Team Balancing Bot.
Represents a player with their Discord information, Steam nickname, and ELO ratings.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set

class Position(Enum):
    """Enum representing player positions in team games."""
    FLANK = "flank"
    POCKET = "pocket"
    ANY = "any"
    
    @classmethod
    def from_string(cls, position_str: str) -> "Position":
        """Convert a string to a Position enum value."""
        position_str = position_str.lower()
        for position in cls:
            if position.value == position_str:
                return position
        return cls.ANY  # Default to ANY if not recognized

@dataclass
class Player:
    """
    Represents a player in the Age of Empires 2 community.
    """
    # Discord information
    discord_id: int
    discord_name: str
    
    # Steam information
    steam_nickname: Optional[str] = None
    
    # ELO ratings
    elo_1v1: Optional[int] = None
    elo_team: Optional[int] = None
    
    # Player preferences
    preferred_position: Position = Position.ANY
    preferred_civs: Set[str] = field(default_factory=set)
    
    # Metadata
    registered_at: datetime = field(default_factory=datetime.utcnow)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    
    # Performance metrics
    games_played: int = 0
    games_won: int = 0
    
    # Position-specific performance
    position_performance: Dict[Position, Dict[str, float]] = field(default_factory=lambda: {
        Position.FLANK: {"games": 0, "wins": 0},
        Position.POCKET: {"games": 0, "wins": 0},
    })
    
    # Civilization performance
    civ_performance: Dict[str, Dict[str, float]] = field(default_factory=dict)
    
    # Tags for player characteristics
    tags: Set[str] = field(default_factory=set)
    
    def update_elo(self, elo_1v1: Optional[int] = None, elo_team: Optional[int] = None) -> None:
        """
        Update the player's ELO ratings.
        
        Args:
            elo_1v1: The player's 1v1 ELO rating.
            elo_team: The player's team game ELO rating.
        """
        if elo_1v1 is not None:
            self.elo_1v1 = elo_1v1
        if elo_team is not None:
            self.elo_team = elo_team
        self.last_updated = datetime.utcnow()
    
    def set_preferred_position(self, position: Position) -> None:
        """
        Set the player's preferred position.
        
        Args:
            position: The preferred position.
        """
        self.preferred_position = position
    
    def add_preferred_civ(self, civ: str) -> None:
        """
        Add a civilization to the player's preferred civilizations.
        
        Args:
            civ: The civilization to add.
        """
        self.preferred_civs.add(civ)
    
    def remove_preferred_civ(self, civ: str) -> None:
        """
        Remove a civilization from the player's preferred civilizations.
        
        Args:
            civ: The civilization to remove.
        """
        if civ in self.preferred_civs:
            self.preferred_civs.remove(civ)
    
    def add_tag(self, tag: str) -> None:
        """
        Add a tag to the player.
        
        Args:
            tag: The tag to add.
        """
        self.tags.add(tag)
    
    def remove_tag(self, tag: str) -> None:
        """
        Remove a tag from the player.
        
        Args:
            tag: The tag to remove.
        """
        if tag in self.tags:
            self.tags.remove(tag)
    
    def record_game_result(self, won: bool, position: Position, civilization: str) -> None:
        """
        Record the result of a game.
        
        Args:
            won: Whether the player won the game.
            position: The position the player played in.
            civilization: The civilization the player used.
        """
        # Update overall stats
        self.games_played += 1
        if won:
            self.games_won += 1
        
        # Update position-specific stats
        if position in self.position_performance:
            self.position_performance[position]["games"] += 1
            if won:
                self.position_performance[position]["wins"] += 1
        
        # Update civilization-specific stats
        if civilization not in self.civ_performance:
            self.civ_performance[civilization] = {"games": 0, "wins": 0}
        self.civ_performance[civilization]["games"] += 1
        if won:
            self.civ_performance[civilization]["wins"] += 1
    
    def get_win_rate(self) -> float:
        """
        Get the player's overall win rate.
        
        Returns:
            The win rate as a percentage.
        """
        if self.games_played == 0:
            return 0.0
        return (self.games_won / self.games_played) * 100
    
    def get_position_win_rate(self, position: Position) -> float:
        """
        Get the player's win rate for a specific position.
        
        Args:
            position: The position to get the win rate for.
            
        Returns:
            The win rate as a percentage.
        """
        if position not in self.position_performance:
            return 0.0
        
        games = self.position_performance[position]["games"]
        wins = self.position_performance[position]["wins"]
        
        if games == 0:
            return 0.0
        return (wins / games) * 100
    
    def get_civ_win_rate(self, civilization: str) -> float:
        """
        Get the player's win rate for a specific civilization.
        
        Args:
            civilization: The civilization to get the win rate for.
            
        Returns:
            The win rate as a percentage.
        """
        if civilization not in self.civ_performance:
            return 0.0
        
        games = self.civ_performance[civilization]["games"]
        wins = self.civ_performance[civilization]["wins"]
        
        if games == 0:
            return 0.0
        return (wins / games) * 100
    
    def calculate_score(self) -> float:
        """
        Calculate the player's score based on their ELO ratings.
        
        Returns:
            The calculated score.
        """
        from config import ELO_1V1_WEIGHT, ELO_TEAM_WEIGHT
        
        # If either ELO is missing, use the other one
        if self.elo_1v1 is None and self.elo_team is None:
            return 0.0
        elif self.elo_1v1 is None:
            return float(self.elo_team)
        elif self.elo_team is None:
            return float(self.elo_1v1)
        
        # Calculate weighted score
        return (ELO_1V1_WEIGHT * self.elo_1v1) + (ELO_TEAM_WEIGHT * self.elo_team) 
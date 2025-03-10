"""
Civilization model for the Age of Empires 2 Team Balancing Bot.
Represents a civilization with its attributes, strengths, and tier ratings.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set

class Tier(Enum):
    """Enum representing civilization tiers."""
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    
    @classmethod
    def from_string(cls, tier_str: str) -> "Tier":
        """Convert a string to a Tier enum value."""
        tier_str = tier_str.upper()
        for tier in cls:
            if tier.value == tier_str:
                return tier
        return cls.C  # Default to C tier if not recognized

class GamePhase(Enum):
    """Enum representing game phases."""
    EARLY = "early"
    MID = "mid"
    LATE = "late"

class PlayStyle(Enum):
    """Enum representing play styles."""
    AGGRESSIVE = "aggressive"
    DEFENSIVE = "defensive"
    BOOMING = "booming"
    BALANCED = "balanced"

@dataclass
class CivilizationRating:
    """
    Rating for a civilization in a specific position.
    """
    tier: Tier
    score: int  # 1-10 rating
    early_game: int  # 1-10 rating
    mid_game: int  # 1-10 rating
    late_game: int  # 1-10 rating
    
    def __post_init__(self):
        """Validate the ratings."""
        for attr in ["score", "early_game", "mid_game", "late_game"]:
            value = getattr(self, attr)
            if not isinstance(value, int) or value < 1 or value > 10:
                raise ValueError(f"{attr} must be an integer between 1 and 10")

@dataclass
class Civilization:
    """
    Represents a civilization in Age of Empires 2.
    """
    # Basic information
    name: str
    display_name: str  # For display purposes (may include special characters)
    
    # Ratings for different positions
    flank_rating: CivilizationRating
    pocket_rating: CivilizationRating
    
    # Strengths and characteristics
    strengths: Set[str] = field(default_factory=set)  # e.g., "archers", "cavalry", "economy"
    unique_units: List[str] = field(default_factory=list)
    unique_techs: List[str] = field(default_factory=list)
    team_bonus: str = ""
    
    # Play style tags
    play_styles: Set[PlayStyle] = field(default_factory=set)
    
    # Map-specific ratings (map_name -> score 1-10)
    map_ratings: Dict[str, int] = field(default_factory=dict)
    
    # Patch information
    current_patch: str = ""
    patch_history: Dict[str, Dict[str, CivilizationRating]] = field(default_factory=dict)
    
    # Synergies with other civilizations (civ_name -> synergy_score 1-10)
    synergies: Dict[str, int] = field(default_factory=dict)
    
    # Counter civilizations (civ_name -> counter_score 1-10)
    counters: Dict[str, int] = field(default_factory=dict)
    
    def get_best_position(self) -> str:
        """
        Get the best position for this civilization.
        
        Returns:
            "flank" or "pocket" based on which has the higher score.
        """
        if self.flank_rating.score > self.pocket_rating.score:
            return "flank"
        elif self.pocket_rating.score > self.flank_rating.score:
            return "pocket"
        else:
            # If scores are equal, check tiers
            flank_tier_value = list(Tier).index(self.flank_rating.tier)
            pocket_tier_value = list(Tier).index(self.pocket_rating.tier)
            
            if flank_tier_value < pocket_tier_value:  # Lower index = higher tier
                return "flank"
            else:
                return "pocket"
    
    def get_rating_for_position(self, position: str) -> CivilizationRating:
        """
        Get the rating for a specific position.
        
        Args:
            position: The position to get the rating for ("flank" or "pocket").
            
        Returns:
            The rating for the specified position.
        """
        if position.lower() == "flank":
            return self.flank_rating
        elif position.lower() == "pocket":
            return self.pocket_rating
        else:
            raise ValueError(f"Invalid position: {position}. Must be 'flank' or 'pocket'.")
    
    def get_best_phase(self) -> GamePhase:
        """
        Get the game phase where this civilization is strongest.
        
        Returns:
            The strongest game phase.
        """
        # Get the best position's ratings
        best_pos = self.get_best_position()
        rating = self.get_rating_for_position(best_pos)
        
        # Find the highest rated phase
        phases = {
            GamePhase.EARLY: rating.early_game,
            GamePhase.MID: rating.mid_game,
            GamePhase.LATE: rating.late_game
        }
        
        return max(phases.items(), key=lambda x: x[1])[0]
    
    def get_best_maps(self, limit: int = 3) -> List[str]:
        """
        Get the best maps for this civilization.
        
        Args:
            limit: The maximum number of maps to return.
            
        Returns:
            A list of map names, sorted by rating.
        """
        sorted_maps = sorted(self.map_ratings.items(), key=lambda x: x[1], reverse=True)
        return [map_name for map_name, _ in sorted_maps[:limit]]
    
    def get_best_synergies(self, limit: int = 3) -> List[str]:
        """
        Get the civilizations that synergize best with this one.
        
        Args:
            limit: The maximum number of civilizations to return.
            
        Returns:
            A list of civilization names, sorted by synergy rating.
        """
        sorted_synergies = sorted(self.synergies.items(), key=lambda x: x[1], reverse=True)
        return [civ_name for civ_name, _ in sorted_synergies[:limit]]
    
    def get_best_counters(self, limit: int = 3) -> List[str]:
        """
        Get the civilizations that this civilization counters best.
        
        Args:
            limit: The maximum number of civilizations to return.
            
        Returns:
            A list of civilization names, sorted by counter rating.
        """
        sorted_counters = sorted(self.counters.items(), key=lambda x: x[1], reverse=True)
        return [civ_name for civ_name, _ in sorted_counters[:limit]]
    
    def is_good_for_map(self, map_name: str, threshold: int = 7) -> bool:
        """
        Check if this civilization is good for a specific map.
        
        Args:
            map_name: The name of the map.
            threshold: The minimum rating to be considered good.
            
        Returns:
            True if the civilization is good for the map, False otherwise.
        """
        return self.map_ratings.get(map_name, 0) >= threshold
    
    def has_synergy_with(self, civ_name: str, threshold: int = 7) -> bool:
        """
        Check if this civilization has good synergy with another civilization.
        
        Args:
            civ_name: The name of the other civilization.
            threshold: The minimum synergy rating to be considered good.
            
        Returns:
            True if the civilizations have good synergy, False otherwise.
        """
        return self.synergies.get(civ_name, 0) >= threshold 
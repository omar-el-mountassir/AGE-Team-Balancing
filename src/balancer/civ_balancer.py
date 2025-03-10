"""
Civilization Balancer for the Age of Empires 2 Team Balancing Bot.
Suggests civilizations for players based on their position, preferences, and map.
"""

import random
from typing import Dict, List, Optional, Set, Tuple

from src.models.civilization import Civilization, Tier
from src.models.player import Player, Position
from src.models.team import Team, TeamMember
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CivilizationBalancer:
    """
    Class for suggesting civilizations for players.
    """
    
    def __init__(self, civilizations: Dict[str, Civilization]):
        """
        Initialize the civilization balancer.
        
        Args:
            civilizations: A dictionary mapping civilization names to Civilization objects.
        """
        self.civilizations = civilizations
    
    def get_civilization_tier(self, civ_name: str, position: Position) -> Tier:
        """
        Get the tier of a civilization for a specific position.
        
        Args:
            civ_name: The name of the civilization.
            position: The position to get the tier for.
            
        Returns:
            The tier of the civilization for the position.
        """
        if civ_name not in self.civilizations:
            return Tier.C  # Default to C tier if not found
        
        civ = self.civilizations[civ_name]
        
        if position == Position.FLANK:
            return civ.flank_rating.tier
        elif position == Position.POCKET:
            return civ.pocket_rating.tier
        else:
            # For ANY position, return the better of the two tiers
            flank_tier_value = list(Tier).index(civ.flank_rating.tier)
            pocket_tier_value = list(Tier).index(civ.pocket_rating.tier)
            
            return civ.flank_rating.tier if flank_tier_value <= pocket_tier_value else civ.pocket_rating.tier
    
    def get_civilization_score(self, civ_name: str, position: Position) -> int:
        """
        Get the score of a civilization for a specific position.
        
        Args:
            civ_name: The name of the civilization.
            position: The position to get the score for.
            
        Returns:
            The score of the civilization for the position.
        """
        if civ_name not in self.civilizations:
            return 5  # Default to middle score if not found
        
        civ = self.civilizations[civ_name]
        
        if position == Position.FLANK:
            return civ.flank_rating.score
        elif position == Position.POCKET:
            return civ.pocket_rating.score
        else:
            # For ANY position, return the better of the two scores
            return max(civ.flank_rating.score, civ.pocket_rating.score)
    
    def get_civilizations_for_position(self, position: Position, tier_threshold: Tier = Tier.B) -> List[str]:
        """
        Get civilizations suitable for a specific position.
        
        Args:
            position: The position to get civilizations for.
            tier_threshold: The minimum tier to include.
            
        Returns:
            A list of civilization names suitable for the position.
        """
        tier_values = {tier: i for i, tier in enumerate(Tier)}
        threshold_value = tier_values[tier_threshold]
        
        suitable_civs = []
        
        for civ_name, civ in self.civilizations.items():
            tier = self.get_civilization_tier(civ_name, position)
            tier_value = tier_values[tier]
            
            if tier_value <= threshold_value:  # Lower value = higher tier
                suitable_civs.append(civ_name)
        
        return suitable_civs
    
    def get_civilizations_for_map(self, map_name: str, threshold: int = 7) -> List[str]:
        """
        Get civilizations suitable for a specific map.
        
        Args:
            map_name: The name of the map.
            threshold: The minimum rating to be considered suitable.
            
        Returns:
            A list of civilization names suitable for the map.
        """
        suitable_civs = []
        
        for civ_name, civ in self.civilizations.items():
            if civ.is_good_for_map(map_name, threshold):
                suitable_civs.append(civ_name)
        
        return suitable_civs
    
    def suggest_civilization(
        self, 
        player: Player, 
        position: Position, 
        map_name: Optional[str] = None,
        team_civs: Optional[List[str]] = None,
        enemy_civs: Optional[List[str]] = None,
        tier_threshold: Tier = Tier.B
    ) -> str:
        """
        Suggest a civilization for a player.
        
        Args:
            player: The player to suggest a civilization for.
            position: The position the player will play.
            map_name: The name of the map, if known.
            team_civs: Civilizations already chosen by teammates.
            enemy_civs: Civilizations chosen by enemies.
            tier_threshold: The minimum tier to consider.
            
        Returns:
            The name of the suggested civilization.
        """
        team_civs = team_civs or []
        enemy_civs = enemy_civs or []
        
        # Get civilizations suitable for the position
        position_civs = set(self.get_civilizations_for_position(position, tier_threshold))
        
        # If map is specified, filter by map suitability
        if map_name:
            map_civs = set(self.get_civilizations_for_map(map_name))
            candidates = position_civs.intersection(map_civs)
            
            # If no civilizations match both criteria, fall back to position-suitable civs
            if not candidates:
                candidates = position_civs
        else:
            candidates = position_civs
        
        # Filter out civilizations already chosen by teammates
        candidates = candidates - set(team_civs)
        
        # If player has preferred civilizations, prioritize them
        preferred_candidates = candidates.intersection(player.preferred_civs)
        if preferred_candidates:
            return random.choice(list(preferred_candidates))
        
        # Look for civilizations with good synergy with team civs
        if team_civs:
            synergy_scores = {}
            for civ_name in candidates:
                if civ_name not in self.civilizations:
                    continue
                
                civ = self.civilizations[civ_name]
                synergy_score = sum(civ.synergies.get(team_civ, 0) for team_civ in team_civs)
                synergy_scores[civ_name] = synergy_score
            
            # Get civilizations with above-average synergy
            if synergy_scores:
                avg_synergy = sum(synergy_scores.values()) / len(synergy_scores)
                good_synergy_civs = [civ for civ, score in synergy_scores.items() if score > avg_synergy]
                
                if good_synergy_civs:
                    return random.choice(good_synergy_civs)
        
        # Look for civilizations that counter enemy civs
        if enemy_civs:
            counter_scores = {}
            for civ_name in candidates:
                if civ_name not in self.civilizations:
                    continue
                
                civ = self.civilizations[civ_name]
                counter_score = sum(civ.counters.get(enemy_civ, 0) for enemy_civ in enemy_civs)
                counter_scores[civ_name] = counter_score
            
            # Get civilizations with above-average counter potential
            if counter_scores:
                avg_counter = sum(counter_scores.values()) / len(counter_scores)
                good_counter_civs = [civ for civ, score in counter_scores.items() if score > avg_counter]
                
                if good_counter_civs:
                    return random.choice(good_counter_civs)
        
        # If we still have candidates, choose one randomly
        if candidates:
            return random.choice(list(candidates))
        
        # If no suitable civilization found, return a random civilization
        return random.choice(list(self.civilizations.keys()))
    
    def suggest_team_civilizations(
        self, 
        team: Team, 
        map_name: Optional[str] = None,
        enemy_civs: Optional[List[str]] = None,
        tier_threshold: Tier = Tier.B
    ) -> Dict[int, str]:
        """
        Suggest civilizations for an entire team.
        
        Args:
            team: The team to suggest civilizations for.
            map_name: The name of the map, if known.
            enemy_civs: Civilizations chosen by enemies.
            tier_threshold: The minimum tier to consider.
            
        Returns:
            A dictionary mapping player Discord IDs to suggested civilizations.
        """
        suggestions = {}
        team_civs = []
        
        # Sort members by how strongly they prefer specific civilizations
        sorted_members = sorted(
            team.members,
            key=lambda m: len(m.player.preferred_civs),
            reverse=True
        )
        
        for member in sorted_members:
            suggested_civ = self.suggest_civilization(
                member.player,
                member.position,
                map_name,
                team_civs,
                enemy_civs,
                tier_threshold
            )
            
            suggestions[member.player.discord_id] = suggested_civ
            team_civs.append(suggested_civ)
        
        return suggestions
    
    def suggest_balanced_team_civilizations(
        self,
        teams: List[Team],
        map_name: Optional[str] = None,
        tier_threshold: Tier = Tier.B
    ) -> Dict[int, str]:
        """
        Suggest balanced civilizations for all teams.
        
        Args:
            teams: The teams to suggest civilizations for.
            map_name: The name of the map, if known.
            tier_threshold: The minimum tier to consider.
            
        Returns:
            A dictionary mapping player Discord IDs to suggested civilizations.
        """
        all_suggestions = {}
        
        # First pass: suggest civilizations for each team
        team_civs = {i: [] for i in range(len(teams))}
        
        for i, team in enumerate(teams):
            # Get civilizations chosen by other teams
            enemy_civs = []
            for j, other_team in enumerate(teams):
                if j != i:
                    enemy_civs.extend(team_civs[j])
            
            # Suggest civilizations for this team
            suggestions = self.suggest_team_civilizations(
                team,
                map_name,
                enemy_civs,
                tier_threshold
            )
            
            all_suggestions.update(suggestions)
            team_civs[i] = list(suggestions.values())
        
        return all_suggestions 
"""
Team model for the Age of Empires 2 Team Balancing Bot.
Represents a team of players with their positions and civilizations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

from src.models.player import Player, Position

@dataclass
class TeamMember:
    """
    Represents a member of a team with their position and civilization.
    """
    player: Player
    position: Position
    civilization: Optional[str] = None
    
    def __hash__(self) -> int:
        """Hash based on the player's Discord ID."""
        return hash(self.player.discord_id)

@dataclass
class Team:
    """
    Represents a team in Age of Empires 2.
    """
    members: List[TeamMember] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def add_member(self, player: Player, position: Position, civilization: Optional[str] = None) -> None:
        """
        Add a member to the team.
        
        Args:
            player: The player to add.
            position: The position the player will play.
            civilization: The civilization the player will use.
        """
        # Check if player is already in the team
        for member in self.members:
            if member.player.discord_id == player.discord_id:
                # Update existing member
                member.position = position
                if civilization:
                    member.civilization = civilization
                return
        
        # Add new member
        self.members.append(TeamMember(player, position, civilization))
    
    def remove_member(self, player_id: int) -> bool:
        """
        Remove a member from the team.
        
        Args:
            player_id: The Discord ID of the player to remove.
            
        Returns:
            True if the player was removed, False otherwise.
        """
        for i, member in enumerate(self.members):
            if member.player.discord_id == player_id:
                self.members.pop(i)
                return True
        return False
    
    def get_member(self, player_id: int) -> Optional[TeamMember]:
        """
        Get a member of the team.
        
        Args:
            player_id: The Discord ID of the player to get.
            
        Returns:
            The team member, or None if not found.
        """
        for member in self.members:
            if member.player.discord_id == player_id:
                return member
        return None
    
    def get_members_by_position(self, position: Position) -> List[TeamMember]:
        """
        Get all members of the team with a specific position.
        
        Args:
            position: The position to filter by.
            
        Returns:
            A list of team members with the specified position.
        """
        return [member for member in self.members if member.position == position]
    
    def get_size(self) -> int:
        """
        Get the number of members in the team.
        
        Returns:
            The number of members.
        """
        return len(self.members)
    
    def calculate_team_score(self) -> float:
        """
        Calculate the team's score based on the scores of its members.
        
        Returns:
            The calculated score.
        """
        if not self.members:
            return 0.0
        
        return sum(member.player.calculate_score() for member in self.members)
    
    def calculate_position_scores(self) -> Dict[Position, float]:
        """
        Calculate the team's score for each position.
        
        Returns:
            A dictionary mapping positions to scores.
        """
        scores = {Position.FLANK: 0.0, Position.POCKET: 0.0}
        
        for member in self.members:
            if member.position in scores:
                scores[member.position] += member.player.calculate_score()
        
        return scores
    
    def get_average_elo(self, elo_type: str = "both") -> float:
        """
        Get the average ELO of the team.
        
        Args:
            elo_type: The type of ELO to average. Can be "1v1", "team", or "both".
            
        Returns:
            The average ELO.
        """
        if not self.members:
            return 0.0
        
        valid_members = 0
        total_elo = 0.0
        
        for member in self.members:
            if elo_type == "1v1" and member.player.elo_1v1 is not None:
                total_elo += member.player.elo_1v1
                valid_members += 1
            elif elo_type == "team" and member.player.elo_team is not None:
                total_elo += member.player.elo_team
                valid_members += 1
            elif elo_type == "both":
                score = member.player.calculate_score()
                if score > 0:
                    total_elo += score
                    valid_members += 1
        
        if valid_members == 0:
            return 0.0
        
        return total_elo / valid_members
    
    def get_team_composition_hash(self) -> int:
        """
        Get a hash representing the team composition (players only, not positions or civs).
        Useful for comparing team compositions.
        
        Returns:
            A hash of the team composition.
        """
        # Sort player IDs to ensure consistent hashing
        player_ids = sorted(member.player.discord_id for member in self.members)
        return hash(tuple(player_ids))
    
    def get_team_composition_with_positions_hash(self) -> int:
        """
        Get a hash representing the team composition including positions.
        
        Returns:
            A hash of the team composition with positions.
        """
        # Sort by player ID for consistent hashing
        composition = sorted(
            (member.player.discord_id, member.position.value) 
            for member in self.members
        )
        return hash(tuple(map(tuple, composition)))
    
    def get_team_composition_full_hash(self) -> int:
        """
        Get a hash representing the full team composition including positions and civilizations.
        
        Returns:
            A hash of the full team composition.
        """
        # Sort by player ID for consistent hashing
        composition = sorted(
            (member.player.discord_id, member.position.value, member.civilization or "")
            for member in self.members
        )
        return hash(tuple(map(tuple, composition))) 
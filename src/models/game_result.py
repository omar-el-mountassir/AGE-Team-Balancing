"""
Game Result model for the Age of Empires 2 Team Balancing Bot.
Represents the result of a game, including teams, map, and outcome.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

from src.models.team import Team

@dataclass
class GameResult:
    """
    Represents the result of a game in Age of Empires 2.
    """
    # Teams that participated
    teams: List[Team]
    
    # Game information
    map_name: str
    game_mode: str  # e.g., "Random Map", "Death Match", etc.
    game_type: str  # e.g., "2v2", "3v3", "4v4"
    
    # Result information
    winning_team_index: int  # Index of the winning team in the teams list
    game_duration_minutes: Optional[int] = None
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    reported_by: Optional[int] = None  # Discord ID of the user who reported the result
    
    # Additional information
    notes: str = ""
    tags: Set[str] = field(default_factory=set)
    
    def get_winning_team(self) -> Team:
        """
        Get the winning team.
        
        Returns:
            The winning team.
        """
        if 0 <= self.winning_team_index < len(self.teams):
            return self.teams[self.winning_team_index]
        raise ValueError(f"Invalid winning team index: {self.winning_team_index}")
    
    def get_losing_teams(self) -> List[Team]:
        """
        Get the losing teams.
        
        Returns:
            A list of losing teams.
        """
        return [team for i, team in enumerate(self.teams) if i != self.winning_team_index]
    
    def get_all_players(self) -> List[Tuple[int, str, str, str, bool]]:
        """
        Get all players who participated in the game.
        
        Returns:
            A list of tuples containing (discord_id, discord_name, position, civilization, won).
        """
        players = []
        
        for team_index, team in enumerate(self.teams):
            won = team_index == self.winning_team_index
            
            for member in team.members:
                players.append((
                    member.player.discord_id,
                    member.player.discord_name,
                    member.position.value,
                    member.civilization or "Unknown",
                    won
                ))
        
        return players
    
    def get_team_composition_description(self) -> str:
        """
        Get a description of the team composition.
        
        Returns:
            A string describing the team composition.
        """
        description = f"{self.game_type} on {self.map_name}\n"
        
        for i, team in enumerate(self.teams):
            team_name = f"Team {i+1}"
            if i == self.winning_team_index:
                team_name += " (Winner)"
            
            description += f"\n{team_name}:\n"
            
            for member in team.members:
                civ = member.civilization or "Unknown"
                description += f"- {member.player.discord_name} ({civ}, {member.position.value})\n"
        
        return description
    
    def to_dict(self) -> Dict:
        """
        Convert the game result to a dictionary for storage.
        
        Returns:
            A dictionary representation of the game result.
        """
        return {
            "teams": [
                {
                    "members": [
                        {
                            "player_id": member.player.discord_id,
                            "position": member.position.value,
                            "civilization": member.civilization
                        }
                        for member in team.members
                    ]
                }
                for team in self.teams
            ],
            "map_name": self.map_name,
            "game_mode": self.game_mode,
            "game_type": self.game_type,
            "winning_team_index": self.winning_team_index,
            "game_duration_minutes": self.game_duration_minutes,
            "created_at": self.created_at.isoformat(),
            "reported_by": self.reported_by,
            "notes": self.notes,
            "tags": list(self.tags)
        } 
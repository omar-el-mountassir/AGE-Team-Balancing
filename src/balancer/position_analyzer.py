"""
Position Analyzer for the Age of Empires 2 Team Balancing Bot.
Analyzes player performance in different positions and suggests optimal positions.
"""

from typing import Dict, List, Optional, Set, Tuple

from src.models.player import Player, Position
from src.utils.logger import get_logger

logger = get_logger(__name__)

class PositionAnalyzer:
    """
    Class for analyzing player performance in different positions.
    """
    
    def __init__(self):
        """Initialize the position analyzer."""
        pass
    
    def calculate_position_score(self, player: Player, position: Position) -> float:
        """
        Calculate a score for a player in a specific position.
        
        Args:
            player: The player to calculate the score for.
            position: The position to calculate the score for.
            
        Returns:
            A score representing how well the player performs in the position.
        """
        # Base score is the win rate in the position
        win_rate = player.get_position_win_rate(position)
        
        # If player has no games in this position, use overall win rate
        if win_rate == 0:
            win_rate = player.get_win_rate()
        
        # Adjust score based on player's preference
        preference_bonus = 0
        if player.preferred_position == position:
            preference_bonus = 20  # Significant bonus for preferred position
        elif player.preferred_position == Position.ANY:
            preference_bonus = 5   # Small bonus for flexible players
        
        return win_rate + preference_bonus
    
    def suggest_positions(self, players: List[Player]) -> Dict[int, Position]:
        """
        Suggest optimal positions for a list of players.
        
        Args:
            players: The players to suggest positions for.
            
        Returns:
            A dictionary mapping player Discord IDs to suggested positions.
        """
        suggestions = {}
        
        # First, calculate scores for each player in each position
        scores = {}
        for player in players:
            scores[player.discord_id] = {
                Position.FLANK: self.calculate_position_score(player, Position.FLANK),
                Position.POCKET: self.calculate_position_score(player, Position.POCKET)
            }
        
        # Sort players by the difference in their scores between positions
        # Players with a larger difference have a stronger preference for one position
        sorted_players = sorted(
            players,
            key=lambda p: abs(scores[p.discord_id][Position.FLANK] - scores[p.discord_id][Position.POCKET]),
            reverse=True
        )
        
        # Track assigned positions
        assigned_positions = {Position.FLANK: 0, Position.POCKET: 0}
        
        # Assign positions to players
        for player in sorted_players:
            flank_score = scores[player.discord_id][Position.FLANK]
            pocket_score = scores[player.discord_id][Position.POCKET]
            
            # Determine the best position for this player
            if flank_score > pocket_score:
                best_position = Position.FLANK
                alternative_position = Position.POCKET
            else:
                best_position = Position.POCKET
                alternative_position = Position.FLANK
            
            # Check if we need to balance positions
            flank_count = assigned_positions[Position.FLANK]
            pocket_count = assigned_positions[Position.POCKET]
            
            # If we have too many players in one position, force some to the other position
            if best_position == Position.FLANK and flank_count >= len(players) // 2:
                assigned_position = alternative_position
            elif best_position == Position.POCKET and pocket_count >= len(players) // 2:
                assigned_position = alternative_position
            else:
                assigned_position = best_position
            
            # Assign the position
            suggestions[player.discord_id] = assigned_position
            assigned_positions[assigned_position] += 1
        
        return suggestions
    
    def analyze_team_positions(self, team_players: List[Player]) -> Dict[int, Position]:
        """
        Analyze and suggest optimal positions for a team.
        
        Args:
            team_players: The players in the team.
            
        Returns:
            A dictionary mapping player Discord IDs to suggested positions.
        """
        return self.suggest_positions(team_players)
    
    def get_position_preference_strength(self, player: Player) -> float:
        """
        Calculate how strongly a player prefers a specific position.
        
        Args:
            player: The player to calculate the preference strength for.
            
        Returns:
            A score representing the strength of the player's position preference.
        """
        if player.preferred_position == Position.ANY:
            return 0.0
        
        # Calculate win rates for each position
        flank_win_rate = player.get_position_win_rate(Position.FLANK)
        pocket_win_rate = player.get_position_win_rate(Position.POCKET)
        
        # If player has no games in either position, they have no strong preference
        if flank_win_rate == 0 and pocket_win_rate == 0:
            return 50.0  # Medium strength preference based on explicit setting
        
        # Calculate the difference in win rates
        win_rate_diff = abs(flank_win_rate - pocket_win_rate)
        
        # Combine explicit preference with performance difference
        return 50.0 + win_rate_diff  # Higher value = stronger preference
    
    def get_position_compatibility(self, player1: Player, player2: Player) -> float:
        """
        Calculate how compatible two players are in terms of position preferences.
        
        Args:
            player1: The first player.
            player2: The second player.
            
        Returns:
            A score representing the position compatibility of the players.
            Higher values indicate more compatible preferences.
        """
        # If both players prefer the same position, they are not compatible
        if (player1.preferred_position == player2.preferred_position and 
            player1.preferred_position != Position.ANY):
            return 0.0
        
        # If one player prefers flank and the other prefers pocket, they are perfectly compatible
        if ((player1.preferred_position == Position.FLANK and player2.preferred_position == Position.POCKET) or
            (player1.preferred_position == Position.POCKET and player2.preferred_position == Position.FLANK)):
            return 100.0
        
        # If one player has no preference, compatibility depends on the other player's preference strength
        if player1.preferred_position == Position.ANY:
            return 50.0 + (self.get_position_preference_strength(player2) / 2)
        
        if player2.preferred_position == Position.ANY:
            return 50.0 + (self.get_position_preference_strength(player1) / 2)
        
        # Default case (should not happen with the above conditions)
        return 50.0 
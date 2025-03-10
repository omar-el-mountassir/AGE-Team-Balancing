"""
Team Balancer for the Age of Empires 2 Team Balancing Bot.
Implements algorithms for balancing teams based on player ELO and preferences.
"""

import itertools
import random
from typing import Dict, List, Optional, Set, Tuple

import config
from src.models.player import Player, Position
from src.models.team import Team, TeamMember
from src.utils.logger import get_logger

logger = get_logger(__name__)

class TeamBalancer:
    """
    Class for balancing teams in Age of Empires 2.
    """
    
    def __init__(self):
        """Initialize the team balancer."""
        self.previous_compositions = set()  # Set of team composition hashes
    
    def calculate_player_score(self, player: Player, position: Position) -> float:
        """
        Calculate a player's score based on their ELO ratings and position.
        
        Args:
            player: The player to calculate the score for.
            position: The position the player will play.
            
        Returns:
            The calculated score.
        """
        # Calculate base score from ELO ratings
        base_score = player.calculate_score()
        
        # Apply position factor
        position_factor = 1.0
        
        # If player is in their preferred position, give a bonus
        if position == player.preferred_position:
            position_factor = config.POSITION_FACTOR_MAX
        # If player has no preference, use neutral factor
        elif player.preferred_position == Position.ANY:
            position_factor = 1.0
        # If player is not in their preferred position, apply penalty
        else:
            position_factor = config.POSITION_FACTOR_MIN
        
        # Apply position-specific performance adjustment
        if position in player.position_performance:
            games = player.position_performance[position]["games"]
            if games > 0:
                win_rate = player.position_performance[position]["wins"] / games
                # Small adjustment based on historical performance in this position
                position_factor *= (0.95 + (win_rate * 0.1))  # 0.95 to 1.05 adjustment
        
        return base_score * position_factor
    
    def calculate_team_score(self, team: Team) -> float:
        """
        Calculate a team's total score.
        
        Args:
            team: The team to calculate the score for.
            
        Returns:
            The calculated score.
        """
        return sum(self.calculate_player_score(member.player, member.position) for member in team.members)
    
    def calculate_team_difference(self, teams: List[Team]) -> float:
        """
        Calculate the difference between team scores.
        
        Args:
            teams: The teams to compare.
            
        Returns:
            The absolute difference between team scores.
        """
        if len(teams) < 2:
            return 0.0
        
        scores = [self.calculate_team_score(team) for team in teams]
        return max(scores) - min(scores)
    
    def calculate_team_difference_percentage(self, teams: List[Team]) -> float:
        """
        Calculate the percentage difference between team scores.
        
        Args:
            teams: The teams to compare.
            
        Returns:
            The percentage difference between team scores.
        """
        if len(teams) < 2:
            return 0.0
        
        scores = [self.calculate_team_score(team) for team in teams]
        total_score = sum(scores)
        
        if total_score == 0:
            return 0.0
        
        return ((max(scores) - min(scores)) / total_score) * 100
    
    def is_balanced(self, teams: List[Team]) -> bool:
        """
        Check if teams are balanced.
        
        Args:
            teams: The teams to check.
            
        Returns:
            True if the teams are balanced, False otherwise.
        """
        diff_percent = self.calculate_team_difference_percentage(teams)
        return diff_percent <= config.ACCEPTABLE_TEAM_DIFF_PERCENT
    
    def is_new_composition(self, teams: List[Team]) -> bool:
        """
        Check if a team composition is new (not seen before).
        
        Args:
            teams: The teams to check.
            
        Returns:
            True if the composition is new, False otherwise.
        """
        # Create a hash of the team composition
        composition_hash = hash(tuple(sorted(team.get_team_composition_hash() for team in teams)))
        
        # Check if we've seen this composition before
        is_new = composition_hash not in self.previous_compositions
        
        # Add to previous compositions if it's new
        if is_new:
            self.previous_compositions.add(composition_hash)
            
            # Limit the number of stored compositions to avoid memory issues
            if len(self.previous_compositions) > 100:
                # Remove a random composition
                self.previous_compositions.pop()
        
        return is_new
    
    def generate_team_compositions(
        self, 
        players: List[Player], 
        team_size: int,
        num_compositions: int = 3,
        respect_preferences: bool = True
    ) -> List[List[Team]]:
        """
        Generate balanced team compositions.
        
        Args:
            players: The players to distribute into teams.
            team_size: The number of players per team.
            num_compositions: The number of compositions to generate.
            respect_preferences: Whether to respect player position preferences.
            
        Returns:
            A list of team compositions, where each composition is a list of teams.
        """
        if len(players) % team_size != 0:
            raise ValueError(f"Number of players ({len(players)}) must be divisible by team size ({team_size})")
        
        num_teams = len(players) // team_size
        
        # Generate all possible team combinations
        player_combinations = list(itertools.combinations(players, team_size))
        
        # Filter valid team combinations (teams that can be formed without duplicating players)
        valid_team_combinations = []
        
        for combo in itertools.combinations(player_combinations, num_teams):
            # Check if each player appears exactly once
            player_set = set()
            for team in combo:
                for player in team:
                    player_set.add(player.discord_id)
            
            if len(player_set) == len(players):
                valid_team_combinations.append(combo)
        
        # If there are too many combinations, sample a subset
        max_combinations_to_check = 1000
        if len(valid_team_combinations) > max_combinations_to_check:
            valid_team_combinations = random.sample(valid_team_combinations, max_combinations_to_check)
        
        # Score each combination
        scored_combinations = []
        
        for combo in valid_team_combinations:
            # Create Team objects
            teams = []
            for team_players in combo:
                team = Team()
                
                # Assign positions based on preferences if requested
                if respect_preferences:
                    # Sort players by how strongly they prefer specific positions
                    sorted_players = sorted(
                        team_players,
                        key=lambda p: 0 if p.preferred_position == Position.ANY else 1,
                        reverse=True
                    )
                    
                    # Track assigned positions
                    assigned_positions = set()
                    
                    # First pass: assign players to their preferred positions if available
                    for player in sorted_players:
                        if player.preferred_position != Position.ANY and player.preferred_position not in assigned_positions:
                            team.add_member(player, player.preferred_position)
                            assigned_positions.add(player.preferred_position)
                    
                    # Second pass: assign remaining players to available positions
                    available_positions = [pos for pos in [Position.FLANK, Position.POCKET] if pos not in assigned_positions]
                    unassigned_players = [p for p in team_players if not any(p.discord_id == m.player.discord_id for m in team.members)]
                    
                    for player, position in zip(unassigned_players, available_positions):
                        team.add_member(player, position)
                else:
                    # Randomly assign positions
                    positions = [Position.FLANK, Position.POCKET] * (team_size // 2)
                    if team_size % 2 == 1:
                        positions.append(random.choice([Position.FLANK, Position.POCKET]))
                    
                    random.shuffle(positions)
                    
                    for player, position in zip(team_players, positions):
                        team.add_member(player, position)
                
                teams.append(team)
            
            # Calculate team difference
            diff_percent = self.calculate_team_difference_percentage(teams)
            
            # Check if this is a new composition
            is_new = self.is_new_composition(teams)
            
            # Score the composition (lower is better)
            score = diff_percent * (0.8 if is_new else 1.2)  # Prefer new compositions
            
            scored_combinations.append((teams, score))
        
        # Sort by score (lower is better)
        scored_combinations.sort(key=lambda x: x[1])
        
        # Return the top N compositions
        return [teams for teams, _ in scored_combinations[:num_compositions]]
    
    def suggest_positions(self, players: List[Player]) -> Dict[int, Position]:
        """
        Suggest optimal positions for players.
        
        Args:
            players: The players to suggest positions for.
            
        Returns:
            A dictionary mapping player Discord IDs to suggested positions.
        """
        suggestions = {}
        
        # First, assign players with strong preferences
        for player in players:
            if player.preferred_position != Position.ANY:
                suggestions[player.discord_id] = player.preferred_position
        
        # For remaining players, look at their performance history
        unassigned_players = [p for p in players if p.discord_id not in suggestions]
        
        for player in unassigned_players:
            # Calculate win rates for each position
            flank_win_rate = player.get_position_win_rate(Position.FLANK)
            pocket_win_rate = player.get_position_win_rate(Position.POCKET)
            
            # Suggest the position with the higher win rate
            if flank_win_rate > pocket_win_rate:
                suggestions[player.discord_id] = Position.FLANK
            else:
                suggestions[player.discord_id] = Position.POCKET
        
        return suggestions 
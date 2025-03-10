"""
Data Loader for the Age of Empires 2 Team Balancing Bot.
Loads civilization and map data from JSON files.
"""

import json
import os
from typing import Dict, List, Optional

from src.models.civilization import Civilization, CivilizationRating, Tier, PlayStyle
from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_civilizations() -> Dict[str, Civilization]:
    """
    Load civilization data from the JSON file.
    
    Returns:
        A dictionary mapping civilization names to Civilization objects.
    """
    civilizations = {}
    
    try:
        # Get the path to the civilizations.json file
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "civilizations.json")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Extract civilization data
        for civ_name, civ_data in data["civilizations"].items():
            try:
                # Create flank rating
                flank_data = civ_data["flank_rating"]
                flank_rating = CivilizationRating(
                    tier=Tier.from_string(flank_data["tier"]),
                    score=flank_data["score"],
                    early_game=flank_data["early_game"],
                    mid_game=flank_data["mid_game"],
                    late_game=flank_data["late_game"]
                )
                
                # Create pocket rating
                pocket_data = civ_data["pocket_rating"]
                pocket_rating = CivilizationRating(
                    tier=Tier.from_string(pocket_data["tier"]),
                    score=pocket_data["score"],
                    early_game=pocket_data["early_game"],
                    mid_game=pocket_data["mid_game"],
                    late_game=pocket_data["late_game"]
                )
                
                # Create play styles set
                play_styles = set()
                for style in civ_data.get("play_styles", []):
                    try:
                        play_styles.add(PlayStyle(style))
                    except ValueError:
                        logger.warning(f"Invalid play style: {style} for civilization {civ_name}")
                
                # Create civilization object
                civilization = Civilization(
                    name=civ_data["name"],
                    display_name=civ_data["display_name"],
                    flank_rating=flank_rating,
                    pocket_rating=pocket_rating,
                    strengths=set(civ_data.get("strengths", [])),
                    unique_units=civ_data.get("unique_units", []),
                    unique_techs=civ_data.get("unique_techs", []),
                    team_bonus=civ_data.get("team_bonus", ""),
                    play_styles=play_styles,
                    map_ratings=civ_data.get("map_ratings", {}),
                    current_patch=data["meta"]["patch"],
                    synergies=civ_data.get("synergies", {}),
                    counters=civ_data.get("counters", {})
                )
                
                civilizations[civ_name] = civilization
                
            except KeyError as e:
                logger.error(f"Missing required field for civilization {civ_name}: {e}")
            except Exception as e:
                logger.error(f"Error loading civilization {civ_name}: {e}")
        
        logger.info(f"Loaded {len(civilizations)} civilizations")
        
    except FileNotFoundError:
        logger.error("Civilizations data file not found")
    except json.JSONDecodeError:
        logger.error("Invalid JSON in civilizations data file")
    except Exception as e:
        logger.error(f"Error loading civilizations data: {e}")
    
    return civilizations

def load_maps() -> Dict[str, Dict]:
    """
    Load map data from the JSON file.
    
    Returns:
        A dictionary mapping map names to map data.
    """
    maps = {}
    
    try:
        # Get the path to the maps.json file
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "maps.json")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Extract map data
        maps = data["maps"]
        
        logger.info(f"Loaded {len(maps)} maps")
        
    except FileNotFoundError:
        logger.error("Maps data file not found")
    except json.JSONDecodeError:
        logger.error("Invalid JSON in maps data file")
    except Exception as e:
        logger.error(f"Error loading maps data: {e}")
    
    return maps

def get_recommended_civilizations(map_name: str, position: str) -> List[str]:
    """
    Get recommended civilizations for a specific map and position.
    
    Args:
        map_name: The name of the map.
        position: The position ("flank" or "pocket").
        
    Returns:
        A list of recommended civilization names.
    """
    maps = load_maps()
    
    if map_name not in maps:
        logger.warning(f"Map {map_name} not found")
        return []
    
    map_data = maps[map_name]
    
    if "recommended_civilizations" not in map_data:
        logger.warning(f"No recommended civilizations for map {map_name}")
        return []
    
    if position not in map_data["recommended_civilizations"]:
        logger.warning(f"No recommended civilizations for position {position} on map {map_name}")
        return []
    
    return map_data["recommended_civilizations"][position]

# Singleton instances
_civilizations = None
_maps = None

def get_civilizations() -> Dict[str, Civilization]:
    """
    Get the civilizations data.
    Loads the data if it hasn't been loaded yet.
    
    Returns:
        A dictionary mapping civilization names to Civilization objects.
    """
    global _civilizations
    
    if _civilizations is None:
        _civilizations = load_civilizations()
    
    return _civilizations

def get_maps() -> Dict[str, Dict]:
    """
    Get the maps data.
    Loads the data if it hasn't been loaded yet.
    
    Returns:
        A dictionary mapping map names to map data.
    """
    global _maps
    
    if _maps is None:
        _maps = load_maps()
    
    return _maps 
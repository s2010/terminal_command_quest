"""
Terminal Command Quest - Core Module

Educational terminal game for learning UNIX commands.
"""

__version__ = "1.0.0"
__author__ = "Terminal Command Quest Team"

# Import only working modules
from .level_loader import LevelLoader, Level, LevelValidationError
from .game_engine import GameEngine

__all__ = [
    'LevelLoader',
    'Level', 
    'LevelValidationError',
    'GameEngine'
] 
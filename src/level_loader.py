"""
Level Loader Module

Handles loading, parsing, and validation of quest levels from YAML files.
Provides the core Level class and LevelLoader functionality.
"""

import yaml
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class LevelValidationError(Exception):
    """Raised when level validation fails."""
    pass


class Level:
    """Represents a single quest level with all its properties."""
    
    def __init__(self, data: Dict[str, Any]):
        # Required fields
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.challenge = data['challenge']
        self.expected_command = data['expected_command']
        
        # Optional fields with defaults
        self.category = data.get('category', 'general')
        self.difficulty = data.get('difficulty', 'beginner')
        self.points = data.get('points', 10)
        self.story = data.get('story', '')
        self.expected_output = data.get('expected_output', '')
        self.hints = data.get('hints', [])
        self.rewards = data.get('rewards', [])
        self.setup_commands = data.get('setup_commands', [])
        self.cleanup_commands = data.get('cleanup_commands', [])
        
        # Process command pattern
        self.command_pattern = self._process_command_pattern()
        
        # Validate the level
        self._validate()
    
    def _process_command_pattern(self) -> str:
        """Process the expected command into a regex pattern."""
        if self.expected_command.startswith('regex:'):
            return self.expected_command[6:]  # Remove 'regex:' prefix
        else:
            # Escape special regex characters and create exact match
            escaped = re.escape(self.expected_command)
            return f"^{escaped}$"
    
    def _validate(self):
        """Validate level properties."""
        required_fields = ['id', 'title', 'description', 'challenge', 'expected_command']
        for field in required_fields:
            if not getattr(self, field):
                raise LevelValidationError(f"Level {self.id}: Missing required field '{field}'")
        
        # Validate difficulty
        valid_difficulties = ['beginner', 'intermediate', 'advanced']
        if self.difficulty not in valid_difficulties:
            raise LevelValidationError(f"Level {self.id}: Invalid difficulty '{self.difficulty}'")
        
        # Validate points
        if not isinstance(self.points, int) or self.points < 0:
            raise LevelValidationError(f"Level {self.id}: Points must be a positive integer")
    
    def get_next_hint(self, hint_index: int) -> Optional[str]:
        """Get the next hint for this level."""
        if 0 <= hint_index < len(self.hints):
            return self.hints[hint_index]
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert level back to dictionary format."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty': self.difficulty,
            'points': self.points,
            'story': self.story,
            'challenge': self.challenge,
            'expected_command': self.expected_command,
            'expected_output': self.expected_output,
            'hints': self.hints,
            'rewards': self.rewards,
            'setup_commands': self.setup_commands,
            'cleanup_commands': self.cleanup_commands
        }


class LevelLoader:
    """Loads and manages quest levels from YAML files."""
    
    def __init__(self, levels_file: str = "levels.yaml"):
        self.levels_file = Path(levels_file)
        self.levels: List[Level] = []
        self._load_levels()
    
    def _load_levels(self):
        """Load levels from the YAML file."""
        try:
            if not self.levels_file.exists():
                raise FileNotFoundError(f"Levels file not found: {self.levels_file}")
            
            with open(self.levels_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not isinstance(data, list):
                raise LevelValidationError("Levels file must contain a list of levels")
            
            self.levels = []
            for level_data in data:
                try:
                    level = Level(level_data)
                    self.levels.append(level)
                except LevelValidationError as e:
                    logger.error(f"Failed to load level: {e}")
                    raise
            
            logger.info(f"Loaded {len(self.levels)} levels from {self.levels_file}")
            
        except yaml.YAMLError as e:
            raise LevelValidationError(f"Failed to parse YAML file: {e}")
        except Exception as e:
            raise LevelValidationError(f"Failed to load levels: {e}")
    
    def get_all_levels(self) -> List[Level]:
        """Get all loaded levels."""
        return self.levels.copy()
    
    def get_level_by_id(self, level_id: str) -> Optional[Level]:
        """Get a level by its ID."""
        for level in self.levels:
            if level.id == level_id:
                return level
        return None
    
    def get_levels_by_category(self, category: str) -> List[Level]:
        """Get all levels in a specific category."""
        return [level for level in self.levels if level.category == category]
    
    def get_levels_by_difficulty(self, difficulty: str) -> List[Level]:
        """Get all levels of a specific difficulty."""
        return [level for level in self.levels if level.difficulty == difficulty]
    
    def validate_all_levels(self) -> List[str]:
        """Validate all levels and return any issues."""
        issues = []
        
        # Check for duplicate IDs
        level_ids = [level.id for level in self.levels]
        if len(level_ids) != len(set(level_ids)):
            duplicates = [id for id in level_ids if level_ids.count(id) > 1]
            issues.extend([f"Duplicate level ID: {id}" for id in set(duplicates)])
        
        # Validate individual levels
        for level in self.levels:
            try:
                level._validate()
            except LevelValidationError as e:
                issues.append(str(e))
        
        return issues
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the loaded levels."""
        if not self.levels:
            return {}
        
        categories = set(level.category for level in self.levels)
        difficulties = set(level.difficulty for level in self.levels)
        total_points = sum(level.points for level in self.levels)
        
        return {
            'total_levels': len(self.levels),
            'categories': sorted(categories),
            'difficulties': sorted(difficulties),
            'total_points': total_points,
            'average_points': total_points / len(self.levels) if self.levels else 0
        }
    
    def reload(self):
        """Reload levels from the file."""
        self._load_levels()
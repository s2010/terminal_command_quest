#!/usr/bin/env python3
"""
Progress Tracker - User Progress and Achievement Management

Tracks user progress through levels, manages achievements, and provides statistics.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ProgressTracker:
    """Tracks user progress and achievements."""
    
    def __init__(self, progress_file: str = "progress.json"):
        """Initialize the progress tracker.
        
        Args:
            progress_file: Path to the progress file
        """
        self.progress_file = Path(progress_file)
        self.progress_data = self._load_progress()
    
    def _load_progress(self) -> Dict[str, Any]:
        """Load progress data from file."""
        if not self.progress_file.exists():
            return self._create_default_progress()
        
        try:
            with open(self.progress_file, 'r') as f:
                data = json.load(f)
            return data
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Error loading progress file: {e}")
            return self._create_default_progress()
    
    def _create_default_progress(self) -> Dict[str, Any]:
        """Create default progress structure."""
        return {
            'completed_levels': [],
            'current_level': 0,
            'total_points': 0,
            'achievements': [],
            'stats': {
                'levels_completed': 0,
                'total_commands_run': 0,
                'total_time_played': 0,
                'hints_used': 0,
                'perfect_completions': 0
            },
            'level_history': [],
            'created': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
    
    def save_progress(self) -> bool:
        """Save progress data to file.
        
        Returns:
            True if save was successful, False otherwise
        """
        try:
            self.progress_data['last_updated'] = datetime.now().isoformat()
            
            # Create directory if it doesn't exist
            self.progress_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.progress_file, 'w') as f:
                json.dump(self.progress_data, f, indent=2, default=str)
            
            return True
            
        except IOError as e:
            logger.error(f"Error saving progress: {e}")
            return False
    
    def complete_level(self, level_id: str, points: int, time_taken: float, 
                      hints_used: int = 0, perfect: bool = False) -> None:
        """Mark a level as completed.
        
        Args:
            level_id: The level identifier
            points: Points earned for this level
            time_taken: Time taken to complete the level (seconds)
            hints_used: Number of hints used
            perfect: Whether the level was completed perfectly
        """
        if level_id not in self.progress_data['completed_levels']:
            self.progress_data['completed_levels'].append(level_id)
            self.progress_data['stats']['levels_completed'] += 1
        
        # Update points
        self.progress_data['total_points'] += points
        
        # Update stats
        self.progress_data['stats']['total_time_played'] += time_taken
        self.progress_data['stats']['hints_used'] += hints_used
        
        if perfect:
            self.progress_data['stats']['perfect_completions'] += 1
        
        # Add to history
        completion_record = {
            'level_id': level_id,
            'points': points,
            'time_taken': time_taken,
            'hints_used': hints_used,
            'perfect': perfect,
            'completed_at': datetime.now().isoformat()
        }
        self.progress_data['level_history'].append(completion_record)
        
        # Check for achievements
        self._check_achievements()
        
        # Save progress
        self.save_progress()
    
    def record_command(self, command: str, success: bool) -> None:
        """Record a command execution.
        
        Args:
            command: The command that was executed
            success: Whether the command was successful
        """
        self.progress_data['stats']['total_commands_run'] += 1
        self.save_progress()
    
    def is_level_completed(self, level_id: str) -> bool:
        """Check if a level has been completed.
        
        Args:
            level_id: The level identifier
            
        Returns:
            True if the level has been completed
        """
        return level_id in self.progress_data['completed_levels']
    
    def get_current_level(self) -> int:
        """Get the current level index.
        
        Returns:
            Current level index (0-based)
        """
        return self.progress_data.get('current_level', 0)
    
    def set_current_level(self, level_index: int) -> None:
        """Set the current level index.
        
        Args:
            level_index: The level index to set
        """
        self.progress_data['current_level'] = level_index
        self.save_progress()
    
    def get_total_points(self) -> int:
        """Get total points earned.
        
        Returns:
            Total points earned
        """
        return self.progress_data.get('total_points', 0)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get progress statistics.
        
        Returns:
            Dictionary containing progress statistics
        """
        return self.progress_data.get('stats', {})
    
    def get_achievements(self) -> List[Dict[str, Any]]:
        """Get earned achievements.
        
        Returns:
            List of achievement dictionaries
        """
        return self.progress_data.get('achievements', [])
    
    def _check_achievements(self) -> None:
        """Check for new achievements and award them."""
        stats = self.progress_data['stats']
        achievements = self.progress_data['achievements']
        
        # Achievement definitions
        achievement_checks = [
            {
                'id': 'first_steps',
                'name': 'First Steps',
                'description': 'Complete your first level',
                'condition': lambda s: s['levels_completed'] >= 1
            },
            {
                'id': 'command_master',
                'name': 'Command Master',
                'description': 'Execute 100 commands',
                'condition': lambda s: s['total_commands_run'] >= 100
            },
            {
                'id': 'speed_demon',
                'name': 'Speed Demon',
                'description': 'Complete a level in under 60 seconds',
                'condition': lambda s: any(
                    record['time_taken'] < 60 
                    for record in self.progress_data.get('level_history', [])
                )
            },
            {
                'id': 'perfectionist',
                'name': 'Perfectionist',
                'description': 'Complete 5 levels perfectly (without hints)',
                'condition': lambda s: s['perfect_completions'] >= 5
            },
            {
                'id': 'quest_complete',
                'name': 'Quest Complete',
                'description': 'Complete all available levels',
                'condition': lambda s: s['levels_completed'] >= 6  # Assuming 6 levels
            }
        ]
        
        # Check each achievement
        for achievement in achievement_checks:
            # Skip if already earned
            if any(a['id'] == achievement['id'] for a in achievements):
                continue
            
            # Check condition
            if achievement['condition'](stats):
                new_achievement = {
                    'id': achievement['id'],
                    'name': achievement['name'],
                    'description': achievement['description'],
                    'earned_at': datetime.now().isoformat()
                }
                achievements.append(new_achievement)
                logger.info(f"Achievement unlocked: {achievement['name']}")
    
    def get_level_history(self) -> List[Dict[str, Any]]:
        """Get level completion history.
        
        Returns:
            List of level completion records
        """
        return self.progress_data.get('level_history', [])
    
    def reset_progress(self) -> None:
        """Reset all progress data."""
        self.progress_data = self._create_default_progress()
        self.save_progress()
        logger.info("Progress reset to default state")
    
    def export_progress(self) -> Dict[str, Any]:
        """Export progress data for backup or sharing.
        
        Returns:
            Complete progress data dictionary
        """
        return self.progress_data.copy()
    
    def import_progress(self, progress_data: Dict[str, Any]) -> bool:
        """Import progress data from backup.
        
        Args:
            progress_data: Progress data dictionary to import
            
        Returns:
            True if import was successful
        """
        try:
            # Validate basic structure
            required_keys = ['completed_levels', 'total_points', 'stats']
            for key in required_keys:
                if key not in progress_data:
                    logger.error(f"Invalid progress data: missing key {key}")
                    return False
            
            self.progress_data = progress_data
            self.progress_data['last_updated'] = datetime.now().isoformat()
            
            return self.save_progress()
            
        except Exception as e:
            logger.error(f"Error importing progress: {e}")
            return False
    
    def get_progress_summary(self) -> Dict[str, Any]:
        """Get a summary of current progress.
        
        Returns:
            Dictionary containing progress summary
        """
        stats = self.progress_data['stats']
        
        return {
            'levels_completed': stats['levels_completed'],
            'total_points': self.progress_data['total_points'],
            'total_time_played': stats['total_time_played'],
            'commands_executed': stats['total_commands_run'],
            'achievements_earned': len(self.progress_data['achievements']),
            'perfect_completions': stats['perfect_completions'],
            'hints_used': stats['hints_used'],
            'current_level': self.progress_data['current_level'],
            'last_played': self.progress_data['last_updated']
        } 
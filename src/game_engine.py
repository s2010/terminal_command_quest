"""
Game Engine Module

Minimal version for validation and statistics.
"""

import sys
from typing import Optional
from colorama import Fore, Style, init

from .level_loader import LevelLoader, LevelValidationError

# Initialize colorama
init(autoreset=True)


class GameEngine:
    """Minimal game engine for validation and statistics."""
    
    def __init__(self, levels_file: str = "levels.yaml", work_dir: Optional[str] = None):
        try:
            self.level_loader = LevelLoader(levels_file)
        except (LevelValidationError, FileNotFoundError) as e:
            print(f"{Fore.RED}[ERROR] Failed to initialize: {e}{Style.RESET_ALL}")
            sys.exit(1)
    
    def start_game(self):
        """Start the validation and show statistics."""
        print(f"\n{Fore.CYAN}[QUEST] Terminal Command Quest{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Validating quest levels...{Style.RESET_ALL}")
        
        # Validate levels
        issues = self.level_loader.validate_all_levels()
        
        if issues:
            print(f"{Fore.YELLOW}[WARNING] Found {len(issues)} validation issues:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"{Fore.GREEN}[SUCCESS] All levels are valid!")
            
        # Show statistics
        stats = self.level_loader.get_statistics()
        print(f"\n{Fore.CYAN}Quest Statistics:")
        print(f"  Total Levels: {stats.get('total_levels', 0)}")
        print(f"  Categories: {', '.join(stats.get('categories', []))}")
        print(f"  Total Points: {stats.get('total_points', 0)}")
        print(f"{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}[INFO] Quest system ready for deployment!{Style.RESET_ALL}")
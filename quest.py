#!/usr/bin/env python3
"""
Terminal Command Quest - Main CLI Entry Point

An interactive text-adventure game that teaches UNIX commands through hands-on challenges.
Designed to be easily embedded in GitHub profile READMEs and infinitely extensible.
"""

import argparse
import sys
import os
from pathlib import Path
import logging

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.game_engine import GameEngine
from src.level_loader import LevelLoader, LevelValidationError


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / "quest.log"),
            logging.StreamHandler(sys.stdout) if verbose else logging.NullHandler()
        ]
    )


def cmd_play(args):
    """Start the interactive game."""
    try:
        game = GameEngine(
            levels_file=args.levels_file,
            work_dir=args.work_dir
        )
        game.start_game()
    except KeyboardInterrupt:
        print("\n[QUEST] Game interrupted. Thanks for playing!")
    except Exception as e:
        print(f"[ERROR] Error starting game: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def cmd_validate(args):
    """Validate level definitions."""
    try:
        print("[SEARCH] Validating level definitions...")
        
        level_loader = LevelLoader(args.levels_file)
        issues = level_loader.validate_all_levels()
        
        if issues:
            print(f"[WARNING] Found {len(issues)} validation issues:")
            for issue in issues:
                print(f"  - {issue}")
            return False
        else:
            print("[SUCCESS] All levels are valid!")
            return True
            
    except LevelValidationError as e:
        print(f"[ERROR] Validation failed: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error during validation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


def cmd_stats(args):
    """Show quest statistics."""
    try:
        level_loader = LevelLoader(args.levels_file)
        stats = level_loader.get_statistics()
        
        print("[STATS] Quest Statistics:")
        print(f"  Total Levels: {stats['total_levels']}")
        print(f"  Categories: {', '.join(stats['categories'])}")
        print(f"  Difficulties: {', '.join(stats['difficulties'])}")
        print(f"  Total Points: {stats['total_points']}")
        print(f"  Average Points: {stats['average_points']:.1f}")
        
        if args.levels:
            print("\n[DOCS] Level Details:")
            levels = level_loader.get_all_levels()
            for i, level in enumerate(levels, 1):
                print(f"  {i:2d}. {level.title}")
                print(f"      Category: {level.category}, Difficulty: {level.difficulty}, Points: {level.points}")
        
    except Exception as e:
        print(f"[ERROR] Error generating statistics: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Terminal Command Quest - Learn UNIX commands through interactive adventures",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s play                    # Start the interactive game
  %(prog)s validate               # Validate level definitions
  %(prog)s stats                  # Show quest statistics
        """
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    
    parser.add_argument(
        "-l", "--levels-file",
        default="levels.yaml",
        help="Path to levels configuration file (default: levels.yaml)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Play command
    play_parser = subparsers.add_parser("play", help="Start the interactive game")
    play_parser.add_argument(
        "-w", "--work-dir",
        help="Working directory for command execution"
    )
    play_parser.set_defaults(func=cmd_play)
    
    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate level definitions")
    validate_parser.set_defaults(func=cmd_validate)
    
    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show quest statistics")
    stats_parser.add_argument(
        "--levels",
        action="store_true",
        help="Show detailed level information"
    )
    stats_parser.set_defaults(func=cmd_stats)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.verbose)
    
    # Default to play if no command specified
    if not args.command:
        args.command = "play"
        args.func = cmd_play
    
    # Execute command
    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n[GOODBYE] Goodbye!")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
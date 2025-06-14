#!/usr/bin/env python3
"""
Quest Generator - Documentation and Template Generation

Generates quest documentation, templates, and updates README files.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List
from .level_loader import LevelLoader


class QuestGenerator:
    """Generates quest documentation and templates."""
    
    def __init__(self, levels_file: str = "levels.yaml"):
        """Initialize the quest generator."""
        self.levels_file = levels_file
        self.level_loader = LevelLoader(levels_file)
    
    def generate_quest_documentation(self, output_file: str = "QUEST.md") -> None:
        """Generate comprehensive quest documentation."""
        levels = self.level_loader.get_all_levels()
        stats = self.level_loader.get_statistics()
        
        content = f"""# Terminal Command Quest

An interactive text-adventure game that teaches UNIX commands through hands-on challenges.

## Quest Overview

- **Total Levels**: {stats['total_levels']}
- **Categories**: {', '.join(stats['categories'])}
- **Difficulty Range**: {', '.join(stats['difficulties'])}
- **Total Points Available**: {stats['total_points']}

## Available Levels

"""
        
        for i, level in enumerate(levels, 1):
            content += f"""
### Level {i}: {level.title}

- **Category**: {level.category}
- **Difficulty**: {level.difficulty}
- **Points**: {level.points}
- **Description**: {level.description}

**Challenge**: {level.challenge}

"""
        
        content += """
## Getting Started

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start your quest: `python quest.py play`

## Commands

- `python quest.py play` - Start the interactive game
- `python quest.py validate` - Validate level definitions
- `python quest.py stats` - Show quest statistics

Enjoy your journey through the terminal!
"""
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        print(f"[SUCCESS] Quest documentation generated: {output_file}")
    
    def generate_level_template(self, output_file: str = "level_template.md") -> None:
        """Generate a template for creating new levels."""
        template = """# Level Creation Template

Use this template to create new levels for Terminal Command Quest.

## Level Structure

```yaml
- id: "unique_level_id"
  title: "Level Title"
  category: "Category Name"
  difficulty: "beginner|intermediate|advanced"
  points: 10
  description: "Brief description of what this level teaches"
  objective: "What the user needs to accomplish"
  
  setup:
    - "mkdir test_directory"
    - "touch test_file.txt"
  
  hints:
    - "Use 'ls' to list files"
    - "Try 'ls -la' for detailed information"
  
  validation:
    type: "command_output"
    command: "ls -la"
    expected_patterns:
      - "test_directory"
      - "test_file.txt"
  
  success_message: "Great job! You've completed this level."
```

## Guidelines

1. **Unique IDs**: Each level must have a unique identifier
2. **Progressive Difficulty**: Build on previous concepts
3. **Clear Objectives**: Make it clear what the user needs to do
4. **Helpful Hints**: Provide guidance without giving away the answer
5. **Proper Validation**: Ensure the validation accurately checks success

## Categories

- **navigation**: Basic file system navigation
- **file_operations**: Creating, reading, modifying files
- **permissions**: File and directory permissions
- **text_processing**: Working with text files
- **archiving**: Compression and archiving
- **system**: System information and processes

## Testing Your Level

1. Add your level to `levels.yaml`
2. Run `python quest.py validate` to check syntax
3. Test by playing: `python quest.py play`
4. Get feedback from other users
"""
        
        with open(output_file, 'w') as f:
            f.write(template)
        
        print(f"[SUCCESS] Level template generated: {output_file}")
    
    def update_readme(self, readme_file: str = "README.md") -> None:
        """Update README.md with quest content between markers."""
        if not os.path.exists(readme_file):
            print(f"[WARNING] {readme_file} not found")
            return
        
        with open(readme_file, 'r') as f:
            content = f.read()
        
        # Look for quest markers
        start_marker = "<!-- QUEST-START -->"
        end_marker = "<!-- QUEST-END -->"
        
        if start_marker not in content or end_marker not in content:
            print("[INFO] No quest markers found in README.md")
            return
        
        # Generate quest content
        stats = self.level_loader.get_statistics()
        quest_content = f"""
## Quest Status

- **Total Levels**: {stats['total_levels']}
- **Categories**: {len(stats['categories'])}
- **Total Points**: {stats['total_points']}
- **Status**: Ready to Play!

### Quick Start

```bash
# Clone the repository
git clone https://github.com/s2010/terminal_command_quest.git
cd terminal_command_quest

# Install dependencies
pip install -r requirements.txt

# Start your quest
python quest.py play
```
"""
        
        # Replace content between markers
        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.find(end_marker)
        
        new_content = content[:start_idx] + quest_content + content[end_idx:]
        
        with open(readme_file, 'w') as f:
            f.write(new_content)
        
        print(f"[SUCCESS] Updated {readme_file} with quest content") 
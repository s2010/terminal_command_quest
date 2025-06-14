# Terminal Command Quest

An interactive text-adventure game that teaches UNIX commands through hands-on challenges.

## Quest Overview

- **Total Levels**: 6
- **Categories**: archives, file_operations, permissions, search, text_processing
- **Difficulty Range**: advanced, beginner, intermediate
- **Total Points Available**: 135

## Available Levels


### Level 1: The Home Directory

- **Category**: file_operations
- **Difficulty**: beginner
- **Points**: 10
- **Description**: Learn basic navigation with ls, pwd, and cd commands

**Challenge**: Discover what treasures lie hidden in the quest_treasures directory


### Level 2: The Search Chamber

- **Category**: search
- **Difficulty**: intermediate
- **Points**: 20
- **Description**: Master find and grep commands to locate hidden treasures

**Challenge**: Find all files ending with '.txt' in the search_chamber directory and subdirectories


### Level 3: The Text Editor's Lair

- **Category**: text_processing
- **Difficulty**: beginner
- **Points**: 15
- **Description**: Conquer cat, head, tail, and less commands for text mastery

**Challenge**: Display the contents of the sacred_scroll.txt file in the text_lair directory


### Level 4: The Permission Fortress

- **Category**: permissions
- **Difficulty**: intermediate
- **Points**: 25
- **Description**: Understand chmod, chown, and file permissions

**Challenge**: Make the locked_treasure.txt file readable by everyone using chmod


### Level 5: The Link Laboratory

- **Category**: file_operations
- **Difficulty**: advanced
- **Points**: 30
- **Description**: Connect files and directories with ln and symbolic links

**Challenge**: Create a symbolic link named 'shortcut_to_artifact' in the shortcuts directory that points to the magic_artifact.txt file


### Level 6: The Archive Vault

- **Category**: archives
- **Difficulty**: advanced
- **Points**: 35
- **Description**: Compress and extract files with tar, gzip, and zip

**Challenge**: Create a tar archive named 'treasure_archive.tar' containing all files from the treasure_collection directory


## Getting Started

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Start your quest: `python quest.py play`

## Commands

- `python quest.py play` - Start the interactive game
- `python quest.py validate` - Validate level definitions
- `python quest.py stats` - Show quest statistics

Enjoy your journey through the terminal!

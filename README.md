# [QUEST] Terminal Command Quest

[![Quest Status](https://img.shields.io/badge/Quest%20Status-Ready%20to%20Start-green)](https://github.com/yourusername/terminal_command_quest)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

An **interactive text-adventure game** that teaches UNIX/Linux commands through hands-on challenges. Designed to be easily embedded in GitHub profile READMEs and infinitely extensible with custom levels.

## [START] Quick Start

```bash
# Clone and start your quest
git clone https://github.com/yourusername/terminal_command_quest.git
cd terminal_command_quest
./quest.sh
```

## [TARGET] Features

- **Modular Architecture**: Add new levels via simple YAML files
- **Auto-Evaluation**: Real-time command validation and feedback
- **Progress Tracking**: Persistent progress with achievement badges
- **Educational**: Learn essential UNIX commands through storytelling
- **GitHub Integration**: Auto-updating README content via GitHub Actions
- **Safe Execution**: Sandboxed command evaluation for security

## [DOCS] Game Overview

Navigate through a mysterious digital realm where each location represents a different UNIX command. Solve puzzles, complete challenges, and master the terminal one command at a time.

### Current Levels

1. **Home Directory** - Learn `ls`, `pwd`, `cd`
2. **Search Chamber** - Master `find`, `grep`, `locate`
3. **Text Editor's Lair** - Conquer `cat`, `head`, `tail`, `less`
4. **Permission Fortress** - Understand `chmod`, `chown`, `chgrp`
5. **Link Laboratory** - Connect with `ln`, `symlink`
6. **Archive Vault** - Compress with `tar`, `gzip`, `zip`

## [SETUP] Installation

### Prerequisites
- Python 3.7+
- UNIX-like environment (Linux, macOS, WSL)

### Setup
```bash
git clone https://github.com/yourusername/terminal_command_quest.git
cd terminal_command_quest
pip install -r requirements.txt
chmod +x quest.sh
```

## [QUEST] How to Play

### Start the Quest
```bash
./quest.sh
```

### Available Commands
- `help` - Show available commands
- `hint` - Get a hint for current challenge
- `skip` - Skip current level (with penalty)
- `progress` - View your current progress
- `reset` - Reset your progress
- `exit` - Exit the game

### Game Commands
The game evaluates actual shell commands you type. For example:
```bash
Quest> ls -la
Quest> find . -name "*.txt"
Quest> grep "treasure" file.txt
```

## [SETUP] Extending the Game

### Adding New Levels

Create a new level definition in `levels.yaml`:

```yaml
- id: "my_custom_level"
  title: "The Custom Challenge"
  description: "Learn the mysterious 'example' command"
  story: |
    You discover a strange new command that seems to hold great power...
  setup_commands:
    - "touch example.txt"
    - "echo 'hidden message' > example.txt"
  challenge: "Use the 'cat' command to reveal the hidden message"
  expected_command: "cat example.txt"
  expected_output: "hidden message"
  hints:
    - "Try using 'cat' followed by a filename"
    - "The file you need is called 'example.txt'"
  rewards:
    - "You've unlocked the power of file reading!"
  cleanup_commands:
    - "rm -f example.txt"
```

### Level Configuration Options

| Field | Required | Description |
|-------|----------|-------------|
| `id` | [SUCCESS] | Unique identifier for the level |
| `title` | [SUCCESS] | Display name for the level |
| `description` | [SUCCESS] | Brief description of what will be learned |
| `story` | [SUCCESS] | Narrative text to immerse the player |
| `setup_commands` | No | Commands to run before the challenge |
| `challenge` | [SUCCESS] | The challenge prompt for the player |
| `expected_command` | [SUCCESS] | Command pattern to match (regex supported) |
| `expected_output` | No | Expected output to validate against |
| `hints` | No | Array of progressive hints |
| `rewards` | No | Messages shown upon completion |
| `cleanup_commands` | No | Commands to run after level completion |

### Custom Quest Creation

1. **Fork this repository**
2. **Modify `levels.yaml`** with your custom levels
3. **Update `config.py`** with your quest metadata
4. **Push changes** - GitHub Actions will auto-generate `QUEST.md`
5. **Embed in your README** using the generated content

## [AUTO] GitHub Integration

### Auto-Updating Quest Status

The included GitHub Action (`.github/workflows/quest.yml`) automatically:
- Generates `QUEST.md` from level definitions
- Updates quest status badges
- Validates level configurations
- Publishes quest statistics

### Embedding in Your Profile README

Add this to your GitHub profile README:

```markdown
## [QUEST] Terminal Command Quest

<!-- QUEST-START -->
<!-- This content is auto-generated. Do not edit manually. -->
[Auto-generated content will appear here]
<!-- QUEST-END -->
```

## Architecture

```
src/
 game_engine.py # Core game logic and state management
 level_loader.py # YAML level loading and validation
 command_evaluator.py # Safe command execution and evaluation
 progress_tracker.py # Progress persistence and statistics
 quest_generator.py # Markdown content generation
 cli.py # Command-line interface
```

### Key Components

- **Game Engine**: Manages game state, level progression, and player actions
- **Level Loader**: Parses and validates YAML level definitions
- **Command Evaluator**: Safely executes and evaluates shell commands
- **Progress Tracker**: Persists player progress and generates statistics
- **Quest Generator**: Creates embeddable Markdown content

## Security

- Commands are executed in a restricted environment
- File system access is limited to the quest directory
- Dangerous commands are blocked via allowlist
- User input is sanitized before execution

## Contributing

We welcome contributions! Here's how you can help:

1. **Add New Levels**: Create educational levels for different commands
2. **Improve UX**: Enhance the player experience and interface
3. **Add Features**: Implement new game mechanics or tools
4. **Fix Bugs**: Help us squash those pesky bugs
5. **Documentation**: Improve guides and examples

### Development Setup

```bash
git clone https://github.com/yourusername/terminal_command_quest.git
cd terminal_command_quest
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
python -m pytest # Run tests
```

## [STATS] Quest Statistics

- **Total Levels**: 6
- **Commands Covered**: 20+
- **Average Completion Time**: 45 minutes
- **Difficulty**: Beginner to Intermediate

## Achievements

- **Quest Master**: Complete all levels
- **Speed Runner**: Complete quest in under 30 minutes
- **Perfect Score**: Complete without using hints
- **Explorer**: Discover all easter eggs
- **Level Creator**: Add a custom level

## [DOCS] Educational Value

This quest covers essential UNIX commands that every developer should know:

| Category | Commands | Skills Learned |
|----------|-----------|----------------|
| **Navigation** | `ls`, `cd`, `pwd` | File system basics |
| **File Operations** | `cp`, `mv`, `rm`, `mkdir` | File manipulation |
| **Text Processing** | `cat`, `grep`, `sed`, `awk` | Text analysis |
| **Permissions** | `chmod`, `chown`, `chgrp` | Security fundamentals |
| **Search** | `find`, `locate`, `which` | File discovery |
| **Archives** | `tar`, `gzip`, `zip` | Compression tools |

## Resources

- [UNIX Command Reference](https://www.unix.com/man-page-repository.php)
- [Linux Command Line Tutorial](https://ubuntu.com/tutorials/command-line-for-beginners)
- [Bash Scripting Guide](https://tldp.org/LDP/Bash-Beginners-Guide/html/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by classic text adventure games
- Built for the developer community
- Special thanks to all contributors

---

**Ready to embark on your Terminal Command Quest?** Clone this repo and start your journey to UNIX mastery!
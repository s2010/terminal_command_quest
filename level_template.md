# Level Creation Template

Use this template to create custom levels for Terminal Command Quest.

## Basic Level Structure

```yaml
- id: "your_level_id"
  title: "Your Level Title"
  description: "Brief description of what the level teaches"
  category: "category_name"
  difficulty: "beginner|intermediate|advanced"
  points: 20
  
  story: |
    Write an engaging story that sets the context for your challenge.
    This should immerse the player in the scenario and explain why
    they need to use the specific command you're teaching.
    
    Multiple paragraphs are encouraged to build atmosphere.
  
  setup_commands:
    - "mkdir -p example_directory"
    - "touch example_directory/file1.txt"
    - "echo 'content' > example_directory/file2.txt"
  
  challenge: "Your challenge instruction goes here"
  
  expected_command: "command_to_match"
  # OR for regex matching:
  # expected_command: "regex:pattern.*to.*match"
  
  expected_output: |
    Expected output if you want to validate command results
    (optional)
  
  hints:
    - "First hint - gentle nudge in right direction"
    - "Second hint - more specific guidance"
    - "Third hint - almost give away the answer"
  
  rewards:
    - "Congratulations message for completing the level"
    - "Educational note about what they learned"
    - "Encouragement for next challenges"
  
  cleanup_commands:
    - "rm -rf example_directory"
```

## Field Descriptions

### Required Fields

- **id**: Unique identifier for the level (lowercase, underscores)
- **title**: Display name shown to players
- **description**: Brief explanation of what the level teaches
- **challenge**: The main instruction/task for the player
- **expected_command**: Command pattern the player should execute

### Optional Fields

- **category**: Groups levels by topic (default: "general")
- **difficulty**: "beginner", "intermediate", or "advanced" (default: "beginner")
- **points**: Score value for completing the level (default: 10)
- **story**: Narrative text to engage the player
- **setup_commands**: Commands to run before the challenge starts
- **expected_output**: Validate command output (optional)
- **hints**: Array of progressive hints
- **rewards**: Messages shown upon successful completion
- **cleanup_commands**: Commands to run after level completion

## Categories

Common categories include:
- `file_operations`: ls, cd, cp, mv, mkdir, etc.
- `text_processing`: cat, grep, sed, awk, etc.
- `permissions`: chmod, chown, chgrp
- `search`: find, locate, which
- `archives`: tar, gzip, zip
- `network`: wget, curl, ssh
- `system`: ps, top, kill, df

## Difficulty Guidelines

**Beginner**: 
- Single command usage
- Basic flags/options
- 10-15 points

**Intermediate**:
- Command combinations
- Multiple steps
- 20-25 points

**Advanced**:
- Complex command chains
- Advanced options
- 30+ points

## Command Matching

### Exact Match
```yaml
expected_command: "ls -la"
```

### Regex Pattern
```yaml
expected_command: "regex:ls.*-[la]+.*"
```

This allows flexible matching while ensuring core command usage.

## Tips for Great Levels

1. **Tell a Story**: Make each level feel like part of an adventure
2. **Progressive Hints**: Start general, get more specific
3. **Clear Instructions**: Be explicit about what success looks like
4. **Clean Setup**: Always clean up files you create
5. **Test Thoroughly**: Try your level with different valid commands

## Example: Intermediate Level

```yaml
- id: "process_detective"
  title: "The Process Detective"
  description: "Learn to investigate running processes with ps and grep"
  category: "system"
  difficulty: "intermediate"
  points: 25
  
  story: |
    The System Guardian has detected unusual activity in the digital realm.
    Rogue processes are consuming resources and slowing down the kingdom.
    
    As the newly appointed Process Detective, you must identify which
    processes are currently running and find the suspicious ones.
    
    Your investigation tools: ps (process status) and grep (pattern search).
  
  setup_commands:
    - "# No setup needed - we'll use real system processes"
  
  challenge: "Find all running processes that contain 'python' in their name"
  
  expected_command: "regex:ps.*grep.*python"
  
  hints:
    - "Use 'ps' to list processes and 'grep' to filter results"
    - "Try: ps aux | grep python"
    - "The pipe symbol '|' connects commands together"
  
  rewards:
    - "Excellent detective work! You've identified the processes."
    - "You now understand how to investigate system activity."
    - "The ps and grep commands are essential for system administration."
```

Save your custom levels in `levels.yaml` and run `python3 quest.py validate` to check for errors!
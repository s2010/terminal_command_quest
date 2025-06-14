# Level Creation Template

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

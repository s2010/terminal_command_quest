#!/usr/bin/env python3
"""
Command Evaluator - Safe Command Execution and Validation

Provides sandboxed execution of user commands and validation of results.
"""

import subprocess
import os
import tempfile
import shutil
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import logging

logger = logging.getLogger(__name__)


class CommandEvaluator:
    """Evaluates and executes user commands safely."""
    
    def __init__(self, work_dir: Optional[str] = None):
        """Initialize the command evaluator.
        
        Args:
            work_dir: Working directory for command execution. If None, creates a temp directory.
        """
        if work_dir:
            self.work_dir = Path(work_dir)
            self.work_dir.mkdir(parents=True, exist_ok=True)
        else:
            self.work_dir = Path(tempfile.mkdtemp(prefix="quest_"))
        
        self.original_cwd = os.getcwd()
        
        # List of allowed commands (for safety)
        self.allowed_commands = {
            'ls', 'cat', 'find', 'grep', 'head', 'tail', 'wc', 'sort', 'uniq',
            'mkdir', 'touch', 'cp', 'mv', 'rm', 'chmod', 'chown', 'ln',
            'tar', 'gzip', 'gunzip', 'zip', 'unzip', 'pwd', 'cd', 'echo',
            'which', 'whoami', 'date', 'df', 'du', 'ps', 'top', 'kill'
        }
        
        # Dangerous patterns to block
        self.blocked_patterns = [
            r'sudo\s+',
            r'rm\s+.*-rf\s+/',
            r'>\s*/dev/',
            r'format\s+',
            r'fdisk\s+',
            r'mkfs\s+',
            r'dd\s+.*of=',
            r'rm\s+.*\*',
            r'curl\s+.*\|\s*sh',
            r'wget\s+.*\|\s*sh',
            r'python\s+.*-c.*exec',
            r'eval\s+',
            r'exec\s+',
        ]
    
    def is_command_safe(self, command: str) -> bool:
        """Check if a command is safe to execute.
        
        Args:
            command: The command to check
            
        Returns:
            True if the command is safe, False otherwise
        """
        # Check for blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                logger.warning(f"Blocked dangerous pattern in command: {command}")
                return False
        
        # Extract the base command
        base_command = command.strip().split()[0] if command.strip() else ''
        
        # Check if base command is allowed
        if base_command not in self.allowed_commands:
            logger.warning(f"Command not in allowed list: {base_command}")
            return False
        
        return True
    
    def setup_environment(self, setup_commands: List[str]) -> bool:
        """Set up the environment with the given setup commands.
        
        Args:
            setup_commands: List of setup commands to execute
            
        Returns:
            True if setup was successful, False otherwise
        """
        try:
            os.chdir(self.work_dir)
            
            for cmd in setup_commands:
                if not self.is_command_safe(cmd):
                    logger.error(f"Unsafe setup command: {cmd}")
                    return False
                
                result = subprocess.run(
                    cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    logger.error(f"Setup command failed: {cmd}")
                    logger.error(f"Error: {result.stderr}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up environment: {e}")
            return False
        finally:
            os.chdir(self.original_cwd)
    
    def execute_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute a user command and return the result.
        
        Args:
            command: The command to execute
            timeout: Timeout in seconds
            
        Returns:
            Dictionary containing execution results
        """
        if not self.is_command_safe(command):
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command blocked for security reasons',
                'return_code': -1
            }
        
        try:
            os.chdir(self.work_dir)
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command timed out',
                'return_code': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'return_code': -1
            }
        finally:
            os.chdir(self.original_cwd)
    
    def validate_result(self, validation_config: Dict[str, Any], command_result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate command result against validation configuration.
        
        Args:
            validation_config: Validation configuration from level
            command_result: Result from command execution
            
        Returns:
            Dictionary containing validation results
        """
        validation_type = validation_config.get('type', 'command_output')
        
        if validation_type == 'command_output':
            return self._validate_command_output(validation_config, command_result)
        elif validation_type == 'file_exists':
            return self._validate_file_exists(validation_config)
        elif validation_type == 'file_content':
            return self._validate_file_content(validation_config)
        else:
            return {
                'success': False,
                'message': f'Unknown validation type: {validation_type}'
            }
    
    def _validate_command_output(self, config: Dict[str, Any], result: Dict[str, Any]) -> Dict[str, Any]:
        """Validate command output against expected patterns."""
        if not result['success']:
            return {
                'success': False,
                'message': 'Command execution failed'
            }
        
        expected_patterns = config.get('expected_patterns', [])
        output = result['stdout']
        
        for pattern in expected_patterns:
            if pattern not in output:
                return {
                    'success': False,
                    'message': f'Expected pattern not found: {pattern}'
                }
        
        return {
            'success': True,
            'message': 'Command output validation successful'
        }
    
    def _validate_file_exists(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that specified files exist."""
        files = config.get('files', [])
        
        try:
            os.chdir(self.work_dir)
            
            for file_path in files:
                if not Path(file_path).exists():
                    return {
                        'success': False,
                        'message': f'Required file not found: {file_path}'
                    }
            
            return {
                'success': True,
                'message': 'File existence validation successful'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error validating file existence: {e}'
            }
        finally:
            os.chdir(self.original_cwd)
    
    def _validate_file_content(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate file content against expected patterns."""
        file_path = config.get('file')
        expected_patterns = config.get('expected_patterns', [])
        
        try:
            os.chdir(self.work_dir)
            
            if not Path(file_path).exists():
                return {
                    'success': False,
                    'message': f'File not found: {file_path}'
                }
            
            with open(file_path, 'r') as f:
                content = f.read()
            
            for pattern in expected_patterns:
                if pattern not in content:
                    return {
                        'success': False,
                        'message': f'Expected pattern not found in file: {pattern}'
                    }
            
            return {
                'success': True,
                'message': 'File content validation successful'
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': f'Error validating file content: {e}'
            }
        finally:
            os.chdir(self.original_cwd)
    
    def cleanup(self):
        """Clean up temporary files and directories."""
        try:
            os.chdir(self.original_cwd)
            if self.work_dir.exists() and str(self.work_dir).startswith('/tmp/quest_'):
                shutil.rmtree(self.work_dir)
        except Exception as e:
            logger.warning(f"Error cleaning up work directory: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup() 
"""
Shared File Utilities
====================

Common file handling functions to eliminate duplication
and provide consistent file operations across components.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


def safe_json_load(file_path: Union[str, Path], 
                  default: Any = None,
                  encoding: str = 'utf-8') -> Any:
    """
    Safely load JSON file with error handling.
    
    Args:
        file_path: Path to JSON file
        default: Default value if file doesn't exist or is invalid
        encoding: File encoding
        
    Returns:
        Parsed JSON data or default value
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, IOError) as e:
        if default is not None:
            return default
        print(f"Warning: Failed to load JSON from {file_path}: {e}")
        return {}


def safe_json_save(data: Any,
                  file_path: Union[str, Path],
                  encoding: str = 'utf-8',
                  indent: int = 2,
                  ensure_dir: bool = True) -> bool:
    """
    Safely save data to JSON file with error handling.
    
    Args:
        data: Data to save
        file_path: Path to save file
        encoding: File encoding
        indent: JSON indentation
        ensure_dir: Whether to create parent directories
        
    Returns:
        True if successful, False otherwise
    """
    try:
        file_path = Path(file_path)
        
        if ensure_dir:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        return True
        
    except (IOError, TypeError) as e:
        print(f"Warning: Failed to save JSON to {file_path}: {e}")
        return False


def ensure_directory(dir_path: Union[str, Path],
                    create_if_missing: bool = True) -> bool:
    """
    Ensure directory exists and is accessible.
    
    Args:
        dir_path: Directory path to check/create
        create_if_missing: Whether to create if missing
        
    Returns:
        True if directory exists and is accessible
    """
    try:
        dir_path = Path(dir_path)
        
        if dir_path.exists():
            if dir_path.is_dir():
                return True
            else:
                print(f"Warning: {dir_path} exists but is not a directory")
                return False
        
        if create_if_missing:
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        
        return False
        
    except (OSError, PermissionError) as e:
        print(f"Warning: Failed to ensure directory {dir_path}: {e}")
        return False


def find_files_by_pattern(directory: Union[str, Path],
                         pattern: str,
                         recursive: bool = True) -> List[Path]:
    """
    Find files matching a pattern in directory.
    
    Args:
        directory: Directory to search
        pattern: File pattern to match (e.g., "*.json")
        recursive: Whether to search recursively
        
    Returns:
        List of matching file paths
    """
    try:
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            return []
        
        if recursive:
            return list(dir_path.rglob(pattern))
        else:
            return list(dir_path.glob(pattern))
            
    except (OSError, PermissionError):
        return []


def get_file_size(file_path: Union[str, Path]) -> Optional[int]:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes or None if error
    """
    try:
        return Path(file_path).stat().st_size
    except (OSError, FileNotFoundError):
        return None


def read_text_file(file_path: Union[str, Path],
                  encoding: str = 'utf-8',
                  fallback_encoding: str = 'latin-1') -> Optional[str]:
    """
    Read text file with encoding fallback.
    
    Args:
        file_path: Path to text file
        encoding: Primary encoding to try
        fallback_encoding: Fallback encoding
        
    Returns:
        File contents or None if error
    """
    for enc in [encoding, fallback_encoding]:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read()
        except (UnicodeDecodeError, UnicodeError):
            continue
        except (FileNotFoundError, IOError):
            return None
    
    print(f"Warning: Failed to read {file_path} with encodings {encoding}, {fallback_encoding}")
    return None


def write_text_file(content: str,
                   file_path: Union[str, Path],
                   encoding: str = 'utf-8',
                   ensure_dir: bool = True) -> bool:
    """
    Write text content to file.
    
    Args:
        content: Text content to write
        file_path: Path to save file
        encoding: File encoding
        ensure_dir: Whether to create parent directories
        
    Returns:
        True if successful, False otherwise
    """
    try:
        file_path = Path(file_path)
        
        if ensure_dir:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return True
        
    except (IOError, UnicodeError) as e:
        print(f"Warning: Failed to write text to {file_path}: {e}")
        return False


def copy_file(source: Union[str, Path],
             destination: Union[str, Path],
             overwrite: bool = False) -> bool:
    """
    Copy file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        overwrite: Whether to overwrite existing file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        import shutil
        
        source_path = Path(source)
        dest_path = Path(destination)
        
        if not source_path.exists():
            print(f"Warning: Source file {source} does not exist")
            return False
        
        if dest_path.exists() and not overwrite:
            print(f"Warning: Destination {destination} exists and overwrite=False")
            return False
        
        # Ensure destination directory exists
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(source_path, dest_path)
        return True
        
    except (IOError, OSError) as e:
        print(f"Warning: Failed to copy {source} to {destination}: {e}")
        return False


def get_project_root(marker_files: List[str] = None) -> Optional[Path]:
    """
    Find project root directory by looking for marker files.
    
    Args:
        marker_files: List of files that indicate project root
        
    Returns:
        Path to project root or None if not found
    """
    if marker_files is None:
        marker_files = ['.git', 'pyproject.toml', 'setup.py', 'package.json', 'requirements.txt']
    
    current_path = Path.cwd()
    
    # Check current directory and parents
    for path in [current_path] + list(current_path.parents):
        for marker in marker_files:
            if (path / marker).exists():
                return path
    
    return None
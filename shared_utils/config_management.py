"""
Shared Configuration Management Utilities
========================================

Common configuration loading and environment variable handling
to eliminate duplication across components.
"""

import os
import json
import yaml
from typing import Dict, Any, Optional, Union
from pathlib import Path


class ConfigManager:
    """Shared configuration management for all components."""
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = Path(config_dir) if config_dir else Path.cwd()
        self._config_cache = {}
    
    def load_config(self, 
                   config_name: str,
                   config_type: str = 'auto',
                   use_cache: bool = True) -> Dict[str, Any]:
        """
        Load configuration from file with caching.
        
        Args:
            config_name: Name of config file (with or without extension)
            config_type: Type of config ('json', 'yaml', or 'auto')
            use_cache: Whether to use cached version if available
            
        Returns:
            Configuration dictionary
        """
        cache_key = f"{config_name}_{config_type}"
        
        if use_cache and cache_key in self._config_cache:
            return self._config_cache[cache_key]
        
        # Find config file
        config_path = self._find_config_file(config_name, config_type)
        if not config_path:
            return {}
        
        # Load based on file type
        try:
            if config_path.suffix.lower() in ['.yml', '.yaml']:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f) or {}
            elif config_path.suffix.lower() == '.json':
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            # Cache the result
            if use_cache:
                self._config_cache[cache_key] = config
            
            return config
            
        except Exception as e:
            print(f"Warning: Failed to load config {config_path}: {e}")
            return {}
    
    def _find_config_file(self, config_name: str, config_type: str) -> Optional[Path]:
        """
        Find configuration file with various extensions.
        
        Args:
            config_name: Base name of config file
            config_type: Preferred config type
            
        Returns:
            Path to config file or None if not found
        """
        # Add extension if not present
        if '.' not in config_name:
            if config_type == 'json':
                config_name += '.json'
            elif config_type in ['yaml', 'yml']:
                config_name += '.yml'
            else:  # auto
                # Try different extensions
                for ext in ['.yml', '.yaml', '.json']:
                    test_path = self.config_dir / f"{config_name}{ext}"
                    if test_path.exists():
                        return test_path
                return None
        
        config_path = self.config_dir / config_name
        return config_path if config_path.exists() else None
    
    def get_env_var(self, 
                   var_name: str, 
                   default: Any = None,
                   var_type: type = str,
                   required: bool = False) -> Any:
        """
        Get environment variable with type conversion and validation.
        
        Args:
            var_name: Environment variable name
            default: Default value if not found
            var_type: Type to convert to (str, int, float, bool)
            required: Whether variable is required
            
        Returns:
            Environment variable value with proper type
            
        Raises:
            ValueError: If required variable is missing
        """
        value = os.getenv(var_name)
        
        if value is None:
            if required:
                raise ValueError(f"Required environment variable '{var_name}' not set")
            return default
        
        # Type conversion
        try:
            if var_type == bool:
                return value.lower() in ('true', '1', 'yes', 'on')
            elif var_type == int:
                return int(value)
            elif var_type == float:
                return float(value)
            else:
                return str(value)
        except (ValueError, TypeError):
            if required:
                raise ValueError(f"Environment variable '{var_name}' cannot be converted to {var_type.__name__}")
            return default
    
    def merge_configs(self, *configs: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge multiple configuration dictionaries.
        
        Args:
            *configs: Configuration dictionaries to merge
            
        Returns:
            Merged configuration dictionary
        """
        merged = {}
        for config in configs:
            merged.update(config)
        return merged
    
    def validate_config(self, 
                       config: Dict[str, Any], 
                       required_keys: List[str]) -> bool:
        """
        Validate that config contains required keys.
        
        Args:
            config: Configuration dictionary
            required_keys: List of required key names
            
        Returns:
            True if all required keys present
        """
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            print(f"Missing required config keys: {missing_keys}")
            return False
        return True


# Convenience functions for backward compatibility
def load_config(config_name: str, config_dir: Optional[str] = None) -> Dict[str, Any]:
    """Convenience function for loading configuration."""
    manager = ConfigManager(config_dir)
    return manager.load_config(config_name)


def get_env_var(var_name: str, 
               default: Any = None,
               var_type: type = str,
               required: bool = False) -> Any:
    """Convenience function for getting environment variables."""
    manager = ConfigManager()
    return manager.get_env_var(var_name, default, var_type, required)
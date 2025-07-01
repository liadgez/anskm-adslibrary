"""
Shared Utilities for ANSKM-ADSLibrary
====================================

Common utilities used across ad-copy-analyzer and facebook-ads-intelligence components
to eliminate code duplication and improve maintainability.
"""

from .text_processing import TextProcessor, clean_text, extract_features
from .config_management import ConfigManager, load_config, get_env_var
from .http_server import CustomHTTPServer, create_cors_handler
from .file_utils import safe_json_load, safe_json_save, ensure_directory

__version__ = "1.0.0"
__all__ = [
    'TextProcessor',
    'clean_text', 
    'extract_features',
    'ConfigManager',
    'load_config',
    'get_env_var',
    'CustomHTTPServer',
    'create_cors_handler',
    'safe_json_load',
    'safe_json_save',
    'ensure_directory'
]
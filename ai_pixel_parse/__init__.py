"""AI Pixel Parse - Behavioral UI Extraction Package.

This package provides tools and agents for extracting behavioral specifications
from web applications. It focuses on capturing interactive behaviors, validation
rules, and functional patterns rather than visual styling.

Main Components:
    - root_agent: Primary agent for user interaction
    - ui_extractor_agent: Specialized agent for UI extraction
    - extract_ui_tool: Core extraction tool function
    - create_extraction_config: Configuration helper
    - extract_ui_specifications: Main extraction executor
"""

from .agent import root_agent
from .ui_extractor_agent import (
    create_extraction_config,
    extract_ui_specifications,
    extract_ui_tool,
    ui_extractor_agent,
)

__all__ = [
    "root_agent",
    "ui_extractor_agent",
    "extract_ui_tool",
    "create_extraction_config",
    "extract_ui_specifications",
]

__version__ = "1.0.0"

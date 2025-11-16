"""AI Pixel Parse - Behavioral UI Extraction Package.

This package provides tools and agents for extracting behavioral specifications
from web applications. It focuses on capturing interactive behaviors, validation
rules, and functional patterns rather than visual styling.

Main Components:
    - root_agent: Primary agent for user interaction
    - ui_extractor_agent: Specialized agent for UI extraction
    - spec_converter_agent: Converts technical extractions to functional specs
    - extract_ui_tool: Core extraction tool function
    - convert_to_functional_spec_tool: Specification conversion tool
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
from .spec_converter_agent import (
    convert_to_functional_spec_tool,
    spec_converter_agent,
)

__all__ = [
    "root_agent",
    "ui_extractor_agent",
    "spec_converter_agent",
    "extract_ui_tool",
    "convert_to_functional_spec_tool",
    "create_extraction_config",
    "extract_ui_specifications",
]

__version__ = "1.0.0"

"""
ADK Configuration for Web UI

This file configures the agents to be accessible via the ADK web interface.
Run with: adk start

Available agents:
1. ui_extractor_agent - Extract UI specifications from web applications
   Example: "Extract UI from google.com, call it google"

2. spec_converter_agent - Convert technical specs to functional specifications
   Example: "Convert dashboard specs to functional requirements"

3. root_agent - General purpose assistant
"""

from ai_pixel_parse.ui_extractor_agent import ui_extractor_agent
from ai_pixel_parse.spec_converter_agent import spec_converter_agent
from ai_pixel_parse.agent import root_agent


# Export agents for ADK web UI
# These will be available in the agent selector
agents = [ui_extractor_agent, spec_converter_agent, root_agent]

__all__ = ['ui_extractor_agent', 'root_agent', 'agents']

"""
ADK Configuration for Web UI

This file configures the agents to be accessible via the ADK web interface.
Run with: adk start

The ui_extractor_agent has the extract_ui_tool function built-in, so you can
simply chat with it:
    "Extract UI from google.com, call it google"
    "Extract from https://example.com with login"
"""

from ai_pixel_parse.ui_extractor_agent import ui_extractor_agent
from ai_pixel_parse.agent import root_agent


# Export agents for ADK web UI
# These will be available in the agent selector
agents = [ui_extractor_agent, root_agent]

__all__ = ['ui_extractor_agent', 'root_agent', 'agents']

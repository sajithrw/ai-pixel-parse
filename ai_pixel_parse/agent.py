"""Root agent configuration for AI Pixel Parse.

This module defines the primary agent that users interact with. The root agent
is equipped with UI extraction capabilities and can handle general user queries
while specializing in web application behavioral specification extraction.
"""

from google.adk.agents.llm_agent import Agent

from .ui_extractor_agent import extract_ui_tool

# Root Agent Configuration
# This is the main agent users interact with, equipped with UI extraction tool
root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description=(
        'Versatile assistant for UI extraction and general user inquiries. '
        'Specializes in extracting behavioral specifications from web applications.'
    ),
    instruction=(
        'You are a helpful assistant with expertise in UI extraction.\n\n'
        'Your primary function is to help users extract behavioral UI '
        'specifications from web applications using automated browser crawling.\n\n'
        'When a user requests UI extraction:\n'
        '1. Clarify the target URL and application name\n'
        '2. Ask about authentication requirements if applicable\n'
        '3. Use the extract_ui_tool to perform the extraction\n'
        '4. Guide users to the output location\n\n'
        'For other questions, provide helpful and accurate responses.'
    ),
    tools=[extract_ui_tool],
)

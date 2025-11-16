"""
Claude Skills MCP Tools

Progressive disclosure pattern - import only what you need.
See: https://www.anthropic.com/engineering/code-execution-with-mcp

Based on K-Dense AI's Claude Skills MCP Server: https://github.com/K-Dense-AI/claude-skills-mcp
"""

# Server management
from .server import get_server, ensure_connected, call_tool

# Individual tools
from .find_helpful_skills import find_helpful_skills
from .read_skill_document import read_skill_document
from .list_skills import list_skills

__all__ = [
    # Server
    "get_server",
    "ensure_connected",
    "call_tool",
    # Tools
    "find_helpful_skills",
    "read_skill_document",
    "list_skills",
]

#!/usr/bin/env python3
"""
Evolving Knowledge System - MCP Server

Exposes knowledge management workflows as MCP tools for Claude Desktop.

Usage:
    python3 mcp_server/server.py

Configuration in Claude Desktop:
    ~/.config/Claude/claude_desktop_config.json
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from evolving_core.managers.idea_manager import IdeaManager
from evolving_core.managers.knowledge_manager import KnowledgeManager
from evolving_core.utils.ai_client import AIClient


class EvolvingMCPServer:
    """MCP Server for Evolving Knowledge System"""

    def __init__(self, base_path: Path):
        """
        Initialize MCP Server.

        Args:
            base_path: Root path of Evolving system
        """
        self.base_path = base_path
        self.server = Server("evolving-knowledge-system")

        # Initialize AI client
        try:
            self.ai_client = AIClient()
        except ValueError:
            # API key not available - AI features will be disabled
            self.ai_client = None

        self.idea_manager = IdeaManager(base_path, ai_client=self.ai_client)
        self.knowledge_manager = KnowledgeManager(base_path)

        # Register tools
        self._register_tools()

    def _register_tools(self):
        """Register all MCP tools"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="idea_list",
                    description="List all ideas with optional filtering by status, category, or minimum potential score",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "filter_status": {
                                "type": "string",
                                "description": "Filter by status",
                                "enum": ["draft", "active", "paused", "completed", "archived"],
                            },
                            "filter_category": {
                                "type": "string",
                                "description": "Filter by category name",
                            },
                            "min_potential": {
                                "type": "integer",
                                "description": "Minimum potential score (1-10)",
                                "minimum": 1,
                                "maximum": 10,
                            },
                        },
                    },
                ),
                Tool(
                    name="idea_create",
                    description="""Create a new idea with analysis. You (Claude) should analyze the idea and provide:
- category: Choose appropriate category (e.g., 'business/saas', 'tech/automation', 'content/creator')
- potential: Score 1-10 based on market need, feasibility, monetization, uniqueness
- tags: 3-5 relevant tags
- required_skills: Skills needed to implement
- monetization: 'direct', 'indirect', or 'none'
- effort: 'low', 'medium', or 'high'
- analysis_text: 2-3 sentences analyzing strengths and challenges
- next_steps: 3-5 concrete action items

Provide as many analysis fields as possible to create a well-structured idea.""",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Idea title (concise, descriptive)",
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of the idea",
                            },
                            "category": {
                                "type": "string",
                                "description": "Category for this idea (e.g., 'business/saas', 'tech/automation', 'content/creator'). Choose based on the idea's domain.",
                            },
                            "potential": {
                                "type": "integer",
                                "description": "Potential score 1-10. Consider: market need, feasibility, monetization potential, uniqueness, skill-fit.",
                                "minimum": 1,
                                "maximum": 10,
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "3-5 relevant tags for categorization and search",
                            },
                            "required_skills": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Skills required to implement this idea (e.g., 'Python', 'API Development', 'Frontend')",
                            },
                            "monetization": {
                                "type": "string",
                                "description": "Monetization approach",
                                "enum": ["direct", "indirect", "none"],
                            },
                            "effort": {
                                "type": "string",
                                "description": "Estimated effort level",
                                "enum": ["low", "medium", "high"],
                            },
                            "analysis_text": {
                                "type": "string",
                                "description": "Your analysis: 2-3 sentences about the idea's strengths, challenges, and viability",
                            },
                            "next_steps": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "3-5 concrete next steps to develop this idea",
                            },
                        },
                        "required": ["title", "description"],
                    },
                ),
                Tool(
                    name="idea_update",
                    description="Update an existing idea: change status, add progress notes from sessions, document insights/decisions, add related items, or update next steps",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "idea_id": {
                                "type": "string",
                                "description": "ID of the idea to update (e.g., 'idea-0001')",
                            },
                            "status": {
                                "type": "string",
                                "description": "New status for the idea",
                                "enum": ["draft", "active", "paused", "completed", "archived"],
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Tags to add (appends to existing tags)",
                            },
                            "related_ideas": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Related idea IDs to add (e.g., ['idea-0002', 'idea-0003'])",
                            },
                            "related_projects": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Related project names to add",
                            },
                            "session_note": {
                                "type": "string",
                                "description": "Summary of work session or progress update",
                            },
                            "session_type": {
                                "type": "string",
                                "description": "Type of session",
                                "enum": ["brainstorming", "validation", "planning", "implementation", "review"],
                            },
                            "insights": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Key insights discovered during session",
                            },
                            "decisions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Decisions made during session",
                            },
                            "next_steps": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Next steps/action items",
                            },
                        },
                        "required": ["idea_id"],
                    },
                ),
                Tool(
                    name="knowledge_search",
                    description="Search through the entire knowledge base for keywords. Returns matching files from projects, prompts, patterns, learnings, etc.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (keywords to search for)",
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results to return (default: 10)",
                                "default": 10,
                                "minimum": 1,
                                "maximum": 50,
                            },
                        },
                        "required": ["query"],
                    },
                ),
                Tool(
                    name="project_list",
                    description="List all projects in the knowledge base with their metadata and status",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                ),
                Tool(
                    name="read_file",
                    description="Read a specific file from the knowledge base. Provide the path relative to the knowledge/ directory (e.g., 'projects/{project-name}/README.md')",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Path to file relative to knowledge/ directory",
                            },
                        },
                        "required": ["path"],
                    },
                ),
                Tool(
                    name="prompt_add",
                    description="Save a prompt to the knowledge base. Use this when you develop a good prompt and want to save it for reuse.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Prompt name (concise, descriptive)",
                            },
                            "content": {
                                "type": "string",
                                "description": "The actual prompt content",
                            },
                            "category": {
                                "type": "string",
                                "description": "Prompt category",
                                "enum": ["frameworks", "research-agents", "skills", "patterns"],
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional description of what this prompt does",
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional tags for categorization",
                            },
                        },
                        "required": ["name", "content", "category"],
                    },
                ),
                Tool(
                    name="learning_add",
                    description="Document a learning or insight. Use this after sessions or when you discover something worth remembering.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Learning title (what was learned)",
                            },
                            "context": {
                                "type": "string",
                                "description": "Context where this was learned (project name, session, etc.)",
                            },
                            "insight": {
                                "type": "string",
                                "description": "The actual insight or learning",
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional tags",
                            },
                            "confidence": {
                                "type": "integer",
                                "description": "Confidence level 0-100 (default: 85)",
                                "minimum": 0,
                                "maximum": 100,
                            },
                        },
                        "required": ["title", "context", "insight"],
                    },
                ),
                Tool(
                    name="resource_add",
                    description="Save a useful resource, tool, or link. Use this when you find something worth keeping for later.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Resource title",
                            },
                            "url": {
                                "type": "string",
                                "description": "Resource URL",
                            },
                            "description": {
                                "type": "string",
                                "description": "What this resource is/does",
                            },
                            "category": {
                                "type": "string",
                                "description": "Resource type",
                                "enum": ["tool", "link", "inspiration", "reference", "learning-material"],
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional tags",
                            },
                        },
                        "required": ["title", "url", "description"],
                    },
                ),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls"""

            if name == "idea_list":
                return await self._handle_idea_list(arguments)
            elif name == "idea_create":
                return await self._handle_idea_create(arguments)
            elif name == "idea_update":
                return await self._handle_idea_update(arguments)
            elif name == "knowledge_search":
                return await self._handle_knowledge_search(arguments)
            elif name == "project_list":
                return await self._handle_project_list(arguments)
            elif name == "read_file":
                return await self._handle_read_file(arguments)
            elif name == "prompt_add":
                return await self._handle_prompt_add(arguments)
            elif name == "learning_add":
                return await self._handle_learning_add(arguments)
            elif name == "resource_add":
                return await self._handle_resource_add(arguments)

            raise ValueError(f"Unknown tool: {name}")

    async def _handle_idea_list(self, arguments: dict) -> list[TextContent]:
        """
        Handle idea_list tool call.

        Args:
            arguments: Tool arguments

        Returns:
            List with TextContent response
        """
        try:
            # Extract filters from arguments
            filter_status = arguments.get("filter_status")
            filter_category = arguments.get("filter_category")
            min_potential = arguments.get("min_potential")

            # Get ideas using IdeaManager
            ideas = self.idea_manager.list(
                filter_status=filter_status,
                filter_category=filter_category,
                min_potential=min_potential,
            )

            # Get statistics
            stats = self.idea_manager.count()
            categories = self.idea_manager.get_categories()

            # Format response
            if not ideas:
                response = "No ideas found."
                if filter_status or filter_category or min_potential:
                    response += "\n\nFilters applied:"
                    if filter_status:
                        response += f"\n- Status: {filter_status}"
                    if filter_category:
                        response += f"\n- Category: {filter_category}"
                    if min_potential:
                        response += f"\n- Minimum potential: {min_potential}"
            else:
                # Build formatted response
                lines = [f"# Ideas ({len(ideas)} found)"]
                lines.append("")

                # Add statistics
                lines.append("## Statistics")
                lines.append(f"- Total: {stats['total']}")
                lines.append(f"- Draft: {stats['draft']}")
                lines.append(f"- Active: {stats['active']}")
                lines.append(f"- Paused: {stats['paused']}")
                lines.append(f"- Completed: {stats['completed']}")
                lines.append(f"- Archived: {stats['archived']}")
                lines.append("")

                # Add categories
                lines.append("## Categories")
                for cat in categories:
                    count = len([i for i in ideas if i.category == cat])
                    lines.append(f"- {cat}: {count}")
                lines.append("")

                # Add ideas
                lines.append("## Ideas")
                lines.append("")

                for idea in ideas:
                    lines.append(f"### {idea.title}")
                    lines.append(f"**ID**: {idea.id}")
                    lines.append(f"**Status**: {idea.status}")
                    lines.append(f"**Category**: {idea.category}")

                    if idea.potential:
                        lines.append(f"**Potential**: {idea.potential}/10")

                    lines.append(f"**Created**: {idea.created}")
                    lines.append(f"**Updated**: {idea.updated}")
                    lines.append("")
                    lines.append(f"{idea.description}")
                    lines.append("")

                    if idea.tags:
                        lines.append(f"*Tags*: {', '.join(idea.tags)}")
                    if idea.required_skills:
                        lines.append(f"*Required Skills*: {', '.join(idea.required_skills)}")

                    lines.append("")
                    lines.append("---")
                    lines.append("")

                response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except Exception as e:
            error_msg = f"Error listing ideas: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    async def _handle_idea_create(self, arguments: dict) -> list[TextContent]:
        """
        Handle idea_create tool call.

        Args:
            arguments: Tool arguments (from Claude Desktop with analysis data)

        Returns:
            List with TextContent response
        """
        try:
            # Extract required fields
            title = arguments.get("title", "").strip()
            description = arguments.get("description", "").strip()

            if not title:
                return [TextContent(type="text", text="Error: Title is required")]

            if not description:
                return [TextContent(type="text", text="Error: Description is required")]

            # Extract optional analysis fields (provided by Claude Desktop)
            category = arguments.get("category")
            potential = arguments.get("potential")
            tags = arguments.get("tags")
            required_skills = arguments.get("required_skills")
            monetization = arguments.get("monetization")
            effort = arguments.get("effort")
            analysis_text = arguments.get("analysis_text")
            next_steps = arguments.get("next_steps")

            # Create idea with analysis data from Claude Desktop
            idea = self.idea_manager.create(
                title=title,
                description=description,
                category=category,
                potential=potential,
                tags=tags,
                required_skills=required_skills,
                monetization=monetization,
                effort=effort,
                analysis_text=analysis_text,
                next_steps=next_steps,
                use_ai_analysis=False  # Claude Desktop provides analysis
            )

            # Build response
            lines = [f"# ✅ Idea Created: {idea.title}"]
            lines.append("")
            lines.append(f"**ID**: {idea.id}")
            lines.append(f"**Category**: {idea.category}")
            lines.append(f"**Status**: {idea.status}")

            if idea.potential:
                lines.append(f"**Potential Score**: {idea.potential}/10")

            lines.append(f"**Effort**: {idea.effort}")
            lines.append(f"**Monetization**: {idea.monetization}")
            lines.append("")

            if idea.tags:
                lines.append(f"**Tags**: {', '.join(idea.tags)}")

            if idea.required_skills:
                lines.append(f"**Required Skills**: {', '.join(idea.required_skills)}")

            lines.append("")
            lines.append("## Description")
            lines.append(description)
            lines.append("")

            lines.append("---")
            lines.append("")
            lines.append(f"Idea saved to: `ideas/{idea.category.replace('/', '-')}/{idea.id}.md`")
            lines.append("")
            lines.append("You can now:")
            lines.append("- Use `idea_update` to add progress")
            lines.append("- Use `idea_list` to see all ideas")
            lines.append("- Use `read_file` to see the full markdown")

            response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except Exception as e:
            error_msg = f"Error creating idea: {str(e)}\n\n{type(e).__name__}"
            import traceback
            error_msg += f"\n\nTraceback:\n{traceback.format_exc()}"
            return [TextContent(type="text", text=error_msg)]

    async def _handle_idea_update(self, arguments: dict) -> list[TextContent]:
        """
        Handle idea_update tool call.

        Args:
            arguments: Tool arguments

        Returns:
            List with TextContent response
        """
        try:
            idea_id = arguments.get("idea_id", "").strip()

            if not idea_id:
                return [TextContent(type="text", text="Error: idea_id is required")]

            # Extract update parameters
            status = arguments.get("status")
            tags = arguments.get("tags")
            related_ideas = arguments.get("related_ideas")
            related_projects = arguments.get("related_projects")
            session_note = arguments.get("session_note")
            session_type = arguments.get("session_type")
            insights = arguments.get("insights")
            decisions = arguments.get("decisions")
            next_steps = arguments.get("next_steps")

            # Validate at least one update is provided
            has_updates = any([
                status, tags, related_ideas, related_projects,
                session_note, insights, decisions, next_steps
            ])

            if not has_updates:
                return [TextContent(
                    type="text",
                    text="Error: At least one update parameter must be provided (status, tags, session_note, etc.)"
                )]

            # Update idea
            idea = self.idea_manager.update(
                idea_id=idea_id,
                status=status,
                tags=tags,
                related_ideas=related_ideas,
                related_projects=related_projects,
                session_note=session_note,
                session_type=session_type,
                insights=insights,
                decisions=decisions,
                next_steps=next_steps
            )

            # Build response
            lines = [f"# ✅ Idea Updated: {idea.title}"]
            lines.append("")
            lines.append(f"**ID**: {idea.id}")
            lines.append(f"**Status**: {idea.status}")
            lines.append(f"**Category**: {idea.category}")
            lines.append(f"**Updated**: {idea.updated}")
            lines.append("")

            # Show what was updated
            lines.append("## Updates Applied")
            lines.append("")

            if status:
                lines.append(f"- Status changed to: **{status}**")

            if tags:
                lines.append(f"- Added tags: {', '.join(tags)}")

            if related_ideas:
                lines.append(f"- Added related ideas: {', '.join(related_ideas)}")

            if related_projects:
                lines.append(f"- Added related projects: {', '.join(related_projects)}")

            if session_note or insights or decisions or next_steps:
                lines.append(f"- Progress session documented")
                if session_type:
                    lines.append(f"  - Type: {session_type}")
                if insights:
                    lines.append(f"  - {len(insights)} insight(s) recorded")
                if decisions:
                    lines.append(f"  - {len(decisions)} decision(s) documented")
                if next_steps:
                    lines.append(f"  - {len(next_steps)} next step(s) added")

            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(f"Idea file updated: `ideas/{idea.category.replace('/', '-')}/{idea.id}.md`")
            lines.append("")
            lines.append("You can now:")
            lines.append("- Use `read_file` to see the updated idea")
            lines.append("- Use `idea_list` to see all ideas")
            lines.append("- Continue working with `idea_update` for more progress")

            response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except ValueError as e:
            error_msg = f"Error updating idea: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

        except Exception as e:
            error_msg = f"Error updating idea: {str(e)}\n\n{type(e).__name__}"
            import traceback
            error_msg += f"\n\nTraceback:\n{traceback.format_exc()}"
            return [TextContent(type="text", text=error_msg)]

    async def _handle_knowledge_search(self, arguments: dict) -> list[TextContent]:
        """
        Handle knowledge_search tool call.

        Args:
            arguments: Tool arguments

        Returns:
            List with TextContent response
        """
        try:
            query = arguments.get("query", "")
            max_results = arguments.get("max_results", 10)

            if not query:
                return [TextContent(type="text", text="Error: Query parameter is required")]

            # Search knowledge base
            results = self.knowledge_manager.search(query, max_results)

            if not results:
                response = f"No results found for query: '{query}'"
            else:
                lines = [f"# Search Results for: '{query}'"]
                lines.append(f"\nFound {len(results)} results")
                lines.append("")

                for i, result in enumerate(results, 1):
                    lines.append(f"## {i}. {result['title']}")
                    lines.append(f"**Type**: {result['type']}")
                    lines.append(f"**Path**: {result['path']}")
                    lines.append(f"**Relevance Score**: {result['score']}")
                    lines.append("")

                    if result['excerpts']:
                        lines.append("**Excerpts**:")
                        for excerpt in result['excerpts']:
                            lines.append(f"- ...{excerpt}...")
                        lines.append("")

                    lines.append("---")
                    lines.append("")

                response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except Exception as e:
            error_msg = f"Error searching knowledge base: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    async def _handle_project_list(self, arguments: dict) -> list[TextContent]:
        """
        Handle project_list tool call.

        Args:
            arguments: Tool arguments

        Returns:
            List with TextContent response
        """
        try:
            projects = self.knowledge_manager.list_projects()

            if not projects:
                response = "No projects found in knowledge base."
            else:
                lines = [f"# Projects ({len(projects)})"]
                lines.append("")

                for project in projects:
                    title = project.get('title', project['name'])
                    lines.append(f"## {title}")
                    lines.append(f"**Name**: {project['name']}")

                    if 'status' in project:
                        lines.append(f"**Status**: {project['status']}")

                    if 'project_name' in project:
                        lines.append(f"**Project Name**: {project['project_name']}")

                    lines.append(f"**Path**: {project['path']}")
                    lines.append("")

                    # Show other metadata
                    metadata_keys = ['tech_stack', 'tags', 'started', 'completed']
                    for key in metadata_keys:
                        if key in project and project[key]:
                            value = project[key]
                            if isinstance(value, list):
                                value = ', '.join(str(v) for v in value)
                            lines.append(f"**{key.replace('_', ' ').title()}**: {value}")

                    lines.append("")
                    lines.append("---")
                    lines.append("")

                response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except Exception as e:
            error_msg = f"Error listing projects: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    async def _handle_read_file(self, arguments: dict) -> list[TextContent]:
        """
        Handle read_file tool call.

        Args:
            arguments: Tool arguments

        Returns:
            List with TextContent response
        """
        try:
            path = arguments.get("path", "")

            if not path:
                return [TextContent(type="text", text="Error: Path parameter is required")]

            # Read file
            file_data = self.knowledge_manager.read_file(path)

            lines = [f"# {path}"]
            lines.append("")
            lines.append(f"**Type**: {file_data['type']}")
            lines.append(f"**Size**: {file_data['size']} characters")
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(file_data['content'])

            response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except FileNotFoundError as e:
            error_msg = f"File not found: {arguments.get('path')}\n\nTry using knowledge_search to find the file first, or project_list to see available projects."
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            error_msg = f"Error reading file: {str(e)}"
            return [TextContent(type="text", text=error_msg)]

    async def _handle_prompt_add(self, arguments: dict) -> list[TextContent]:
        """
        Handle prompt_add tool call.

        Args:
            arguments: Tool arguments

        Returns:
            List with TextContent response
        """
        try:
            name = arguments.get("name", "").strip()
            content = arguments.get("content", "").strip()
            category = arguments.get("category", "").strip()
            description = arguments.get("description", "").strip()
            tags = arguments.get("tags", [])

            if not name:
                return [TextContent(type="text", text="Error: Name is required")]
            if not content:
                return [TextContent(type="text", text="Error: Content is required")]
            if not category:
                return [TextContent(type="text", text="Error: Category is required")]

            # Add prompt
            result = self.knowledge_manager.add_prompt(
                name=name,
                content=content,
                category=category,
                tags=tags,
                description=description
            )

            # Build response
            lines = [f"# ✅ Prompt Saved: {result['name']}"]
            lines.append("")
            lines.append(f"**Category**: {result['category']}")
            lines.append(f"**Path**: `{result['path']}`")
            lines.append("")

            if tags:
                lines.append(f"**Tags**: {', '.join(tags)}")
                lines.append("")

            lines.append("## Content Preview")
            lines.append(content[:200] + ("..." if len(content) > 200 else ""))
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("You can now:")
            lines.append("- Use `knowledge_search` to find this prompt later")
            lines.append(f"- Read the full prompt using `read_file` with path: `prompts/{category}/{result['safe_name']}.md`")

            response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except ValueError as e:
            error_msg = f"Error: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            error_msg = f"Error adding prompt: {str(e)}"
            import traceback
            error_msg += f"\n\nTraceback:\n{traceback.format_exc()}"
            return [TextContent(type="text", text=error_msg)]

    async def _handle_learning_add(self, arguments: dict) -> list[TextContent]:
        """
        Handle learning_add tool call.

        Args:
            arguments: Tool arguments

        Returns:
            List with TextContent response
        """
        try:
            title = arguments.get("title", "").strip()
            context = arguments.get("context", "").strip()
            insight = arguments.get("insight", "").strip()
            tags = arguments.get("tags", [])
            confidence = arguments.get("confidence", 85)

            if not title:
                return [TextContent(type="text", text="Error: Title is required")]
            if not context:
                return [TextContent(type="text", text="Error: Context is required")]
            if not insight:
                return [TextContent(type="text", text="Error: Insight is required")]

            # Add learning
            result = self.knowledge_manager.add_learning(
                title=title,
                context=context,
                insight=insight,
                tags=tags,
                confidence=confidence
            )

            # Build response
            lines = [f"# ✅ Learning Documented: {result['title']}"]
            lines.append("")
            lines.append(f"**Path**: `{result['path']}`")
            lines.append(f"**Confidence**: {result['confidence']}%")
            lines.append("")

            if tags:
                lines.append(f"**Tags**: {', '.join(tags)}")
                lines.append("")

            lines.append("## Context")
            lines.append(context[:150] + ("..." if len(context) > 150 else ""))
            lines.append("")
            lines.append("## Insight")
            lines.append(insight[:150] + ("..." if len(insight) > 150 else ""))
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("You can now:")
            lines.append("- Use `knowledge_search` to find this learning later")
            lines.append(f"- Read the full learning using `read_file` with path: `learnings/{result['safe_name']}.md`")

            response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except ValueError as e:
            error_msg = f"Error: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            error_msg = f"Error adding learning: {str(e)}"
            import traceback
            error_msg += f"\n\nTraceback:\n{traceback.format_exc()}"
            return [TextContent(type="text", text=error_msg)]

    async def _handle_resource_add(self, arguments: dict) -> list[TextContent]:
        """
        Handle resource_add tool call.

        Args:
            arguments: Tool arguments

        Returns:
            List with TextContent response
        """
        try:
            title = arguments.get("title", "").strip()
            url = arguments.get("url", "").strip()
            description = arguments.get("description", "").strip()
            category = arguments.get("category", "tool").strip()
            tags = arguments.get("tags", [])

            if not title:
                return [TextContent(type="text", text="Error: Title is required")]
            if not url:
                return [TextContent(type="text", text="Error: URL is required")]
            if not description:
                return [TextContent(type="text", text="Error: Description is required")]

            # Add resource
            result = self.knowledge_manager.add_resource(
                title=title,
                url=url,
                description=description,
                category=category,
                tags=tags
            )

            # Build response
            lines = [f"# ✅ Resource Saved: {result['title']}"]
            lines.append("")
            lines.append(f"**URL**: {result['url']}")
            lines.append(f"**Category**: {result['category']}")
            lines.append(f"**Path**: `{result['path']}`")
            lines.append("")

            if tags:
                lines.append(f"**Tags**: {', '.join(tags)}")
                lines.append("")

            lines.append("## Description")
            lines.append(description[:200] + ("..." if len(description) > 200 else ""))
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("You can now:")
            lines.append("- Use `knowledge_search` to find this resource later")
            lines.append(f"- Read the full resource using `read_file` with path: `resources/{result['safe_name']}.md`")

            response = "\n".join(lines)

            return [TextContent(type="text", text=response)]

        except ValueError as e:
            error_msg = f"Error: {str(e)}"
            return [TextContent(type="text", text=error_msg)]
        except Exception as e:
            error_msg = f"Error adding resource: {str(e)}"
            import traceback
            error_msg += f"\n\nTraceback:\n{traceback.format_exc()}"
            return [TextContent(type="text", text=error_msg)]

    async def run(self):
        """Start the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options(),
            )


async def main():
    """Main entry point"""
    # Get base path from environment or use default
    base_path = Path(__file__).parent.parent

    # Create and run server
    server = EvolvingMCPServer(base_path)
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

"""
Idea Manager - Business logic for idea management
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from ..utils.json_db import JSONDatabase
from ..utils.file_ops import FileOps
from ..utils.ai_client import AIClient
from ..models.idea import Idea


class IdeaManager:
    """Manages ideas in the knowledge system"""

    def __init__(self, base_path: Path, ai_client: Optional[AIClient] = None):
        """
        Initialize IdeaManager.

        Args:
            base_path: Root path of Evolving system
            ai_client: AI client for analysis (optional, created if not provided)
        """
        self.base_path = Path(base_path)
        self.db = JSONDatabase(self.base_path)
        self.file_ops = FileOps(self.base_path)
        self.index_path = "ideas/index.json"
        self.ai_client = ai_client

    def list(self, filter_status: Optional[str] = None,
             filter_category: Optional[str] = None,
             min_potential: Optional[int] = None) -> List[Idea]:
        """
        List all ideas with optional filtering.

        Args:
            filter_status: Filter by status (draft|active|paused|completed|archived)
            filter_category: Filter by category
            min_potential: Minimum potential score (1-10)

        Returns:
            List of Idea objects matching filters
        """
        # Read ideas from index
        index_data = self.db.read_json(self.index_path, default={"ideas": []})

        # Handle both old format (list) and new format (dict with "ideas" key)
        if isinstance(index_data, list):
            ideas_data = index_data
        else:
            ideas_data = index_data.get("ideas", [])

        # Convert to Idea objects
        ideas = [Idea.from_dict(data) for data in ideas_data]

        # Apply filters
        if filter_status:
            ideas = [idea for idea in ideas if idea.status == filter_status]

        if filter_category:
            ideas = [idea for idea in ideas if idea.category == filter_category]

        if min_potential is not None:
            ideas = [idea for idea in ideas if idea.potential and idea.potential >= min_potential]

        return ideas

    def get(self, idea_id: str) -> Optional[Idea]:
        """
        Get idea by ID.

        Args:
            idea_id: Idea ID to retrieve

        Returns:
            Idea object or None if not found
        """
        index_data = self.db.read_json(self.index_path, default={"ideas": []})

        # Handle both formats
        if isinstance(index_data, list):
            ideas_data = index_data
        else:
            ideas_data = index_data.get("ideas", [])

        for data in ideas_data:
            if data.get("id") == idea_id:
                return Idea.from_dict(data)

        return None

    def count(self) -> Dict[str, int]:
        """
        Get idea statistics.

        Returns:
            Dictionary with counts by status
        """
        ideas = self.list()

        stats = {
            "total": len(ideas),
            "draft": len([i for i in ideas if i.status == "draft"]),
            "active": len([i for i in ideas if i.status == "active"]),
            "paused": len([i for i in ideas if i.status == "paused"]),
            "completed": len([i for i in ideas if i.status == "completed"]),
            "archived": len([i for i in ideas if i.status == "archived"]),
        }

        return stats

    def get_categories(self) -> List[str]:
        """
        Get all unique categories.

        Returns:
            List of category names
        """
        index_data = self.db.read_json(self.index_path, default={"ideas": []})

        # Handle both formats
        if isinstance(index_data, list):
            ideas_data = index_data
        else:
            ideas_data = index_data.get("ideas", [])

        categories = set(data.get("category", "") for data in ideas_data if data.get("category"))
        return sorted(categories)

    def create(self, title: str, description: str,
               category: Optional[str] = None,
               potential: Optional[int] = None,
               tags: Optional[List[str]] = None,
               required_skills: Optional[List[str]] = None,
               monetization: Optional[str] = None,
               effort: Optional[str] = None,
               analysis_text: Optional[str] = None,
               next_steps: Optional[List[str]] = None,
               use_ai_analysis: bool = False) -> Idea:
        """
        Create a new idea with analysis data.

        Analysis data can be provided directly (e.g., from Claude Desktop)
        or generated via AI API call (legacy, requires API key).

        Args:
            title: Idea title
            description: Idea description
            category: Category (e.g., "business/saas") - if not provided, uses AI or defaults
            potential: Potential score 1-10 - if not provided, uses AI or defaults
            tags: List of tags - if not provided, uses AI or defaults
            required_skills: Required skills - if not provided, uses AI or defaults
            monetization: Monetization type (direct|indirect|none) - if not provided, uses AI or defaults
            effort: Effort level (low|medium|high) - if not provided, uses AI or defaults
            analysis_text: AI-generated analysis text (optional)
            next_steps: List of next steps (optional)
            use_ai_analysis: Use AI API for analysis if no data provided (default: False, requires API key)

        Returns:
            Created Idea object

        Raises:
            ValueError: If AI analysis requested but AI client not available
        """
        # Generate ID
        index_data = self.db.read_json(self.index_path, default={"ideas": [], "last_id": 0})

        # Handle both formats
        if isinstance(index_data, list):
            ideas_data = index_data
            last_id = len(ideas_data)
        else:
            ideas_data = index_data.get("ideas", [])
            last_id = index_data.get("last_id", len(ideas_data))

        new_id = f"idea-{last_id + 1:04d}"

        # Determine if we have external analysis data
        has_external_analysis = any([
            category is not None,
            potential is not None,
            tags is not None,
            required_skills is not None,
            monetization is not None,
            effort is not None
        ])

        # Use provided data, or AI analysis, or defaults
        if has_external_analysis:
            # Use provided analysis data (from Claude Desktop)
            category = category or "uncategorized"
            potential = potential
            tags = tags or []
            required_skills = required_skills or []
            monetization = monetization or "none"
            effort = effort or "medium"
            analysis_text = analysis_text or ""
            next_steps = next_steps or []

        elif use_ai_analysis:
            # Legacy: Use AI API for analysis (requires API key)
            if not self.ai_client:
                raise ValueError("AI client not available. Initialize IdeaManager with AIClient or provide analysis data directly.")

            existing_categories = self.get_categories()
            analysis = self.ai_client.analyze_idea(title, description, existing_categories)

            category = analysis.get("category", "uncategorized")
            potential = analysis.get("potential", 5)
            tags = analysis.get("tags", [])
            required_skills = analysis.get("required_skills", [])
            monetization = analysis.get("monetization", "none")
            effort = analysis.get("effort", "medium")
            analysis_text = analysis.get("analysis_text", "")
            next_steps = analysis.get("next_steps", [])

        else:
            # Defaults (no analysis)
            category = "uncategorized"
            potential = None
            tags = []
            required_skills = []
            monetization = "none"
            effort = "medium"
            analysis_text = ""
            next_steps = []

        # Create Idea object
        idea = Idea(
            id=new_id,
            title=title,
            description=description,
            category=category,
            status="draft",
            potential=potential,
            tags=tags,
            required_skills=required_skills,
            monetization=monetization,
            effort=effort
        )

        # Create markdown file
        category_path = f"ideas/{category.replace('/', '-')}"
        self.file_ops.ensure_dir(category_path)

        md_content = self._build_idea_markdown(idea, analysis_text, next_steps)
        md_path = f"{category_path}/{new_id}.md"
        self.file_ops.write_file(md_path, md_content, backup=False)

        # Update index
        ideas_data.append(idea.to_dict())

        # Save in new format
        new_index = {
            "ideas": ideas_data,
            "categories": self.get_categories(),
            "last_id": last_id + 1,
            "stats": self.count()
        }
        self.db.write_json(self.index_path, new_index, backup=True)

        return idea

    def _build_idea_markdown(self, idea: Idea, analysis_text: str = "",
                            next_steps: List[str] = None) -> str:
        """Build markdown content for idea file"""

        lines = [idea.to_frontmatter(), ""]
        lines.append(f"# {idea.title}")
        lines.append("")

        lines.append("## Beschreibung")
        lines.append(idea.description)
        lines.append("")

        if analysis_text:
            lines.append("## Analyse")
            lines.append(analysis_text)
            lines.append("")

        lines.append("## Skills")
        if idea.required_skills:
            for skill in idea.required_skills:
                lines.append(f"- {skill}")
        else:
            lines.append("- (noch nicht analysiert)")
        lines.append("")

        lines.append("## Fortschritt")
        lines.append("(noch keine Updates)")
        lines.append("")

        if next_steps:
            lines.append("## Nächste Schritte")
            for step in next_steps:
                lines.append(f"- [ ] {step}")
            lines.append("")

        lines.append("## Erkenntnisse")
        lines.append("(noch keine Erkenntnisse)")
        lines.append("")

        lines.append("## Verbindungen")
        lines.append("(noch keine Verbindungen)")
        lines.append("")

        return "\n".join(lines)

    def update(self, idea_id: str,
               status: Optional[str] = None,
               tags: Optional[List[str]] = None,
               related_ideas: Optional[List[str]] = None,
               related_projects: Optional[List[str]] = None,
               session_note: Optional[str] = None,
               session_type: Optional[str] = None,
               insights: Optional[List[str]] = None,
               decisions: Optional[List[str]] = None,
               next_steps: Optional[List[str]] = None) -> Idea:
        """
        Update an existing idea.

        Args:
            idea_id: ID of idea to update
            status: New status (draft|active|paused|completed|archived)
            tags: Tags to add (appends to existing)
            related_ideas: Related idea IDs to add
            related_projects: Related project names to add
            session_note: Summary of work session
            session_type: Type of session (brainstorming|validation|planning|implementation)
            insights: Key insights from session
            decisions: Decisions made during session
            next_steps: Next steps to add/replace

        Returns:
            Updated Idea object

        Raises:
            ValueError: If idea not found or invalid status
        """
        # Load idea from index
        idea = self.get(idea_id)
        if not idea:
            raise ValueError(f"Idea not found: {idea_id}")

        # Validate status if provided
        valid_statuses = ["draft", "active", "paused", "completed", "archived"]
        if status and status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(valid_statuses)}")

        # Find markdown file
        category_path = f"ideas/{idea.category.replace('/', '-')}"
        md_path = f"{category_path}/{idea_id}.md"

        if not self.file_ops.file_exists(md_path):
            raise ValueError(f"Idea markdown file not found: {md_path}")

        # Read existing markdown
        md_content = self.file_ops.read_file(md_path)

        # Parse frontmatter and content
        frontmatter, body = self._parse_markdown(md_content)

        # Update frontmatter fields
        if status:
            frontmatter["status"] = status
            idea.status = status

        if tags:
            existing_tags = frontmatter.get("tags", [])
            new_tags = list(set(existing_tags + tags))
            frontmatter["tags"] = new_tags
            idea.tags = new_tags

        if related_ideas:
            existing = frontmatter.get("related_ideas", [])
            new_related = list(set(existing + related_ideas))
            frontmatter["related_ideas"] = new_related
            idea.related_ideas = new_related

        if related_projects:
            existing = frontmatter.get("related_projects", [])
            new_related = list(set(existing + related_projects))
            frontmatter["related_projects"] = new_related
            idea.related_projects = new_related

        # Always update timestamp
        today = datetime.now().strftime("%Y-%m-%d")
        frontmatter["updated"] = today
        idea.updated = today

        # Update body sections
        new_body = body

        # Add session to Fortschritt section
        if session_note or insights or decisions or next_steps:
            new_body = self._add_progress_entry(
                new_body,
                session_note=session_note,
                session_type=session_type,
                insights=insights,
                decisions=decisions,
                next_steps=next_steps
            )

        # Build updated markdown
        updated_md = self._build_markdown_with_frontmatter(frontmatter, new_body)

        # Write back
        self.file_ops.write_file(md_path, updated_md, backup=True)

        # Update index.json
        self._update_index(idea)

        return idea

    def _parse_markdown(self, content: str) -> tuple[Dict[str, Any], str]:
        """Parse markdown into frontmatter dict and body content"""
        lines = content.split('\n')

        if not lines or lines[0] != '---':
            return {}, content

        # Find end of frontmatter
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i] == '---':
                end_idx = i
                break

        if end_idx == -1:
            return {}, content

        # Parse frontmatter
        frontmatter = {}
        frontmatter_lines = lines[1:end_idx]

        for line in frontmatter_lines:
            if ':' not in line:
                continue

            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Parse lists
            if value.startswith('[') and value.endswith(']'):
                list_content = value[1:-1]
                if list_content:
                    items = [item.strip() for item in list_content.split(',')]
                    frontmatter[key] = items
                else:
                    frontmatter[key] = []
            # Parse null
            elif value == 'null':
                frontmatter[key] = None
            # Parse numbers
            elif value.isdigit():
                frontmatter[key] = int(value)
            else:
                frontmatter[key] = value

        # Body is everything after frontmatter
        body = '\n'.join(lines[end_idx + 1:])

        return frontmatter, body

    def _add_progress_entry(self, body: str,
                           session_note: Optional[str] = None,
                           session_type: Optional[str] = None,
                           insights: Optional[List[str]] = None,
                           decisions: Optional[List[str]] = None,
                           next_steps: Optional[List[str]] = None) -> str:
        """Add a progress entry to the Fortschritt section"""

        # Build progress entry
        timestamp = datetime.now().strftime("%Y-%m-%d")
        session_title = f"### Session {timestamp}"
        if session_type:
            session_title += f" - {session_type}"

        entry_lines = ["", session_title, ""]

        if session_note:
            entry_lines.append(session_note)
            entry_lines.append("")

        if insights:
            entry_lines.append("**Erkenntnisse:**")
            for insight in insights:
                entry_lines.append(f"- {insight}")
            entry_lines.append("")

        if decisions:
            entry_lines.append("**Entscheidungen:**")
            for decision in decisions:
                entry_lines.append(f"- {decision}")
            entry_lines.append("")

        if next_steps:
            entry_lines.append("**Nächste Schritte:**")
            for step in next_steps:
                entry_lines.append(f"- [ ] {step}")
            entry_lines.append("")

        entry_text = '\n'.join(entry_lines)

        # Find Fortschritt section
        fortschritt_pattern = r'## Fortschritt\s*\n(.*?)(?=\n## |\Z)'
        match = re.search(fortschritt_pattern, body, re.DOTALL)

        if match:
            current_content = match.group(1).strip()

            # Replace placeholder if exists
            if current_content == "(noch keine Updates)":
                new_content = entry_text.strip()
            else:
                # Append new entry
                new_content = current_content + entry_text

            # Replace in body
            body = re.sub(
                fortschritt_pattern,
                f"## Fortschritt\n\n{new_content}\n\n",
                body,
                flags=re.DOTALL
            )

        return body

    def _build_markdown_with_frontmatter(self, frontmatter: Dict[str, Any], body: str) -> str:
        """Build markdown content from frontmatter dict and body"""
        lines = ["---"]

        for key, value in frontmatter.items():
            if isinstance(value, list):
                if value:
                    lines.append(f"{key}: [{', '.join(str(v) for v in value)}]")
                else:
                    lines.append(f"{key}: []")
            elif value is None:
                lines.append(f"{key}: null")
            else:
                lines.append(f"{key}: {value}")

        lines.append("---")
        lines.append(body)

        return '\n'.join(lines)

    def _update_index(self, idea: Idea) -> None:
        """Update idea in index.json"""
        index_data = self.db.read_json(self.index_path, default={"ideas": []})

        # Handle both formats
        if isinstance(index_data, list):
            ideas_data = index_data
        else:
            ideas_data = index_data.get("ideas", [])

        # Find and update idea
        for i, data in enumerate(ideas_data):
            if data.get("id") == idea.id:
                ideas_data[i] = idea.to_dict()
                break

        # Save in new format
        new_index = {
            "ideas": ideas_data,
            "categories": self.get_categories(),
            "last_id": index_data.get("last_id", len(ideas_data)),
            "stats": self.count()
        }
        self.db.write_json(self.index_path, new_index, backup=True)

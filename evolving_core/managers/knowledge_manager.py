"""
Knowledge Manager - Business logic for knowledge base operations
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from ..utils.file_ops import FileOps


class KnowledgeManager:
    """Manages knowledge base search and retrieval"""

    def __init__(self, base_path: Path):
        """
        Initialize KnowledgeManager.

        Args:
            base_path: Root path of Evolving system
        """
        self.base_path = Path(base_path)
        self.knowledge_path = self.base_path / "knowledge"
        self.file_ops = FileOps(base_path)

    def search(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Search knowledge base for query.

        Args:
            query: Search query (keywords)
            max_results: Maximum number of results to return

        Returns:
            List of matching files with metadata and excerpts
        """
        results = []
        query_lower = query.lower()
        query_words = query_lower.split()

        # Search in all markdown files
        for md_file in self.knowledge_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding='utf-8')
                content_lower = content.lower()

                # Calculate relevance score
                score = 0
                matches = []

                # Check if all query words are present
                for word in query_words:
                    if word in content_lower:
                        score += content_lower.count(word)
                        # Find context around match
                        pattern = re.compile(f'.{{0,50}}{re.escape(word)}.{{0,50}}', re.IGNORECASE)
                        found_matches = pattern.findall(content)
                        matches.extend(found_matches[:2])  # Max 2 excerpts per word

                if score > 0:
                    # Get relative path from knowledge/
                    relative_path = md_file.relative_to(self.knowledge_path)

                    # Extract title from first line or filename
                    lines = content.split('\n')
                    title = None
                    for line in lines[:10]:  # Check first 10 lines
                        if line.startswith('# '):
                            title = line[2:].strip()
                            break
                    if not title:
                        title = md_file.stem.replace('-', ' ').title()

                    results.append({
                        'path': str(relative_path),
                        'absolute_path': str(md_file),
                        'title': title,
                        'score': score,
                        'excerpts': matches[:3],  # Max 3 excerpts total
                        'type': self._classify_file(md_file)
                    })

            except Exception as e:
                # Skip files that can't be read
                continue

        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)

        return results[:max_results]

    def list_projects(self) -> List[Dict[str, Any]]:
        """
        List all projects in knowledge base.

        Returns:
            List of projects with metadata
        """
        projects = []
        projects_path = self.knowledge_path / "projects"

        if not projects_path.exists():
            return []

        for project_dir in projects_path.iterdir():
            if project_dir.is_dir():
                readme_path = project_dir / "README.md"
                if readme_path.exists():
                    try:
                        content = readme_path.read_text(encoding='utf-8')

                        # Extract metadata from frontmatter or content
                        metadata = self._extract_project_metadata(content)
                        metadata['name'] = project_dir.name
                        metadata['path'] = str(project_dir.relative_to(self.knowledge_path))
                        metadata['absolute_path'] = str(project_dir)

                        projects.append(metadata)

                    except Exception:
                        continue

        return projects

    def read_file(self, relative_path: str) -> Dict[str, Any]:
        """
        Read a file from knowledge base.

        Args:
            relative_path: Path relative to knowledge/ directory

        Returns:
            File content and metadata

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path = self.knowledge_path / relative_path

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")

        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {relative_path}")

        # Security: Ensure path is within knowledge base
        try:
            file_path.relative_to(self.knowledge_path)
        except ValueError:
            raise ValueError(f"Path outside knowledge base: {relative_path}")

        content = file_path.read_text(encoding='utf-8')

        return {
            'path': relative_path,
            'absolute_path': str(file_path),
            'content': content,
            'size': len(content),
            'type': self._classify_file(file_path)
        }

    def _classify_file(self, file_path: Path) -> str:
        """Classify file by location"""
        parts = file_path.parts

        if 'projects' in parts:
            return 'project'
        elif 'prompts' in parts:
            return 'prompt'
        elif 'patterns' in parts:
            return 'pattern'
        elif 'learnings' in parts:
            return 'learning'
        elif 'personal' in parts:
            return 'personal'
        elif 'resources' in parts:
            return 'resource'
        elif 'sessions' in parts:
            return 'session'
        else:
            return 'other'

    def _extract_project_metadata(self, content: str) -> Dict[str, Any]:
        """Extract project metadata from README content"""
        metadata = {}

        # Try to extract from frontmatter
        if content.startswith('---'):
            end_idx = content.find('---', 3)
            if end_idx > 0:
                frontmatter = content[3:end_idx]
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        metadata[key.strip()] = value.strip().strip('"')

        # Extract title from first # heading
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                metadata['title'] = line[2:].strip()
                break

        # Extract status if present
        status_patterns = [
            r'\*\*Status\*\*:\s*(.+)',
            r'Status:\s*(.+)',
        ]
        for pattern in status_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                metadata['status'] = match.group(1).strip()
                break

        return metadata

    def add_prompt(self, name: str, content: str, category: str,
                   tags: List[str] = None, description: str = "") -> Dict[str, Any]:
        """
        Add a new prompt to the knowledge base.

        Args:
            name: Prompt name (used for filename)
            content: Prompt content
            category: Category (frameworks/research-agents/skills/patterns)
            tags: Optional tags
            description: Optional description

        Returns:
            Dictionary with created file info

        Raises:
            ValueError: If category is invalid or file already exists
        """
        # Validate category
        valid_categories = ["frameworks", "research-agents", "skills", "patterns"]
        if category not in valid_categories:
            raise ValueError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")

        # Create safe filename
        safe_name = name.lower().replace(' ', '-').replace('/', '-')
        safe_name = re.sub(r'[^a-z0-9-]', '', safe_name)

        # Check if file exists
        file_path = f"knowledge/prompts/{category}/{safe_name}.md"
        if self.file_ops.file_exists(file_path):
            raise ValueError(f"Prompt already exists: {file_path}\nUse a different name or delete the existing file first.")

        # Build frontmatter
        frontmatter_lines = ["---"]
        frontmatter_lines.append(f'title: "{name}"')
        frontmatter_lines.append(f'type: {category.rstrip("s")}')  # frameworks -> framework
        frontmatter_lines.append(f'category: prompt-engineering')

        if tags:
            tags_str = ", ".join(tags)
            frontmatter_lines.append(f'tags: [{tags_str}]')

        frontmatter_lines.append(f'created: {datetime.now().strftime("%Y-%m-%d")}')
        frontmatter_lines.append(f'status: active')
        frontmatter_lines.append("---")

        # Build content
        md_lines = frontmatter_lines + [""]
        md_lines.append(f"# {name}")
        md_lines.append("")

        if description:
            md_lines.append(description)
            md_lines.append("")
            md_lines.append("---")
            md_lines.append("")

        md_lines.append(content)
        md_lines.append("")

        # Write file
        md_content = "\n".join(md_lines)
        self.file_ops.write_file(file_path, md_content, backup=False)

        return {
            "name": name,
            "path": file_path,
            "category": category,
            "safe_name": safe_name
        }

    def add_learning(self, title: str, context: str, insight: str,
                     tags: List[str] = None, confidence: int = 85) -> Dict[str, Any]:
        """
        Add a new learning to the knowledge base.

        Args:
            title: Learning title
            context: Context where this was learned (project/session)
            insight: The actual learning/insight
            tags: Optional tags
            confidence: Confidence level (0-100, default: 85)

        Returns:
            Dictionary with created file info
        """
        # Create safe filename
        safe_name = title.lower().replace(' ', '-')
        safe_name = re.sub(r'[^a-z0-9-]', '', safe_name)

        # Check if file exists
        file_path = f"knowledge/learnings/{safe_name}.md"
        if self.file_ops.file_exists(file_path):
            raise ValueError(f"Learning already exists: {file_path}\nUse a different title.")

        # Build frontmatter
        frontmatter_lines = ["---"]
        frontmatter_lines.append(f'title: "{title}"')
        frontmatter_lines.append(f'type: learning')
        frontmatter_lines.append(f'context: "{context}"')

        if tags:
            tags_str = ", ".join(tags)
            frontmatter_lines.append(f'tags: [{tags_str}]')

        frontmatter_lines.append(f'confidence: {confidence}%')
        frontmatter_lines.append(f'created: {datetime.now().strftime("%Y-%m-%d")}')
        frontmatter_lines.append("---")

        # Build content
        md_lines = frontmatter_lines + [""]
        md_lines.append(f"# {title}")
        md_lines.append("")
        md_lines.append("## Kontext")
        md_lines.append(context)
        md_lines.append("")
        md_lines.append("## Erkenntnis")
        md_lines.append(insight)
        md_lines.append("")
        md_lines.append("## Anwendung")
        md_lines.append("(Wo kann dies wiederverwendet werden?)")
        md_lines.append("")

        # Write file
        md_content = "\n".join(md_lines)
        self.file_ops.write_file(file_path, md_content, backup=False)

        return {
            "title": title,
            "path": file_path,
            "safe_name": safe_name,
            "confidence": confidence
        }

    def add_resource(self, title: str, url: str, description: str,
                     category: str = "tool", tags: List[str] = None) -> Dict[str, Any]:
        """
        Add a new resource to the knowledge base.

        Args:
            title: Resource title
            url: Resource URL
            description: What this resource is/does
            category: Resource category (tool/link/inspiration/reference)
            tags: Optional tags

        Returns:
            Dictionary with created file info
        """
        # Validate category
        valid_categories = ["tool", "link", "inspiration", "reference", "learning-material"]
        if category not in valid_categories:
            raise ValueError(f"Invalid category. Must be one of: {', '.join(valid_categories)}")

        # Create safe filename
        safe_name = title.lower().replace(' ', '-')
        safe_name = re.sub(r'[^a-z0-9-]', '', safe_name)

        # Check if file exists
        file_path = f"knowledge/resources/{safe_name}.md"
        if self.file_ops.file_exists(file_path):
            raise ValueError(f"Resource already exists: {file_path}\nUse a different title.")

        # Build frontmatter
        frontmatter_lines = ["---"]
        frontmatter_lines.append(f'title: "{title}"')
        frontmatter_lines.append(f'type: resource')
        frontmatter_lines.append(f'category: {category}')
        frontmatter_lines.append(f'url: "{url}"')

        if tags:
            tags_str = ", ".join(tags)
            frontmatter_lines.append(f'tags: [{tags_str}]')

        frontmatter_lines.append(f'added: {datetime.now().strftime("%Y-%m-%d")}')
        frontmatter_lines.append("---")

        # Build content
        md_lines = frontmatter_lines + [""]
        md_lines.append(f"# {title}")
        md_lines.append("")
        md_lines.append(f"**URL**: {url}")
        md_lines.append(f"**Category**: {category}")
        md_lines.append("")
        md_lines.append("## Description")
        md_lines.append(description)
        md_lines.append("")
        md_lines.append("## Usage Notes")
        md_lines.append("(How/when to use this resource)")
        md_lines.append("")

        # Write file
        md_content = "\n".join(md_lines)
        self.file_ops.write_file(file_path, md_content, backup=False)

        return {
            "title": title,
            "path": file_path,
            "url": url,
            "category": category,
            "safe_name": safe_name
        }

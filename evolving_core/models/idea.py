"""
Idea Data Model
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional


@dataclass
class Idea:
    """Represents an idea in the knowledge system"""

    id: str
    title: str
    description: str
    category: str
    status: str = "draft"  # draft|active|paused|completed|archived
    potential: Optional[int] = None  # 1-10
    tags: List[str] = field(default_factory=list)
    required_skills: List[str] = field(default_factory=list)
    related_ideas: List[str] = field(default_factory=list)
    related_projects: List[str] = field(default_factory=list)
    monetization: str = "none"  # direct|indirect|none
    effort: str = "medium"  # low|medium|high
    created: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    updated: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

    def to_frontmatter(self) -> str:
        """Convert to YAML frontmatter string"""
        lines = ["---"]
        for key, value in self.to_dict().items():
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
        return "\n".join(lines)

    @classmethod
    def from_dict(cls, data: dict) -> 'Idea':
        """Create Idea from dictionary"""
        return cls(**data)

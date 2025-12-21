"""
AI Client - Claude API integration for analysis and categorization
"""

import os
from typing import Dict, Any, Optional, List
from anthropic import Anthropic


class AIClient:
    """Client for Claude AI API interactions"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Client.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be provided or set in environment")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Sonnet

    def analyze_idea(self, title: str, description: str,
                     existing_categories: List[str] = None) -> Dict[str, Any]:
        """
        Analyze an idea and provide categorization, potential score, etc.

        Args:
            title: Idea title
            description: Idea description
            existing_categories: List of existing categories for suggestions

        Returns:
            Dictionary with analysis results
        """
        # Build prompt
        prompt = self._build_idea_analysis_prompt(title, description, existing_categories)

        # Call Claude API
        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse response
        response_text = message.content[0].text
        analysis = self._parse_idea_analysis(response_text)

        return analysis

    def _build_idea_analysis_prompt(self, title: str, description: str,
                                    existing_categories: List[str] = None) -> str:
        """Build prompt for idea analysis"""

        categories_context = ""
        if existing_categories:
            categories_context = f"\n\nExisting categories: {', '.join(existing_categories)}"

        prompt = f"""Analyze this idea and provide structured analysis:

**Title**: {title}

**Description**: {description}
{categories_context}

Provide analysis in this EXACT format:

CATEGORY: [Choose from existing categories if relevant, or suggest new category. Format: category/subcategory]
POTENTIAL: [Score 1-10 based on: market need, feasibility, monetization, uniqueness, skill-fit]
TAGS: [3-5 relevant tags, comma-separated]
REQUIRED_SKILLS: [Skills needed, comma-separated]
MONETIZATION: [direct/indirect/none]
EFFORT: [low/medium/high]

ANALYSIS:
[2-3 sentences analyzing the idea's strengths and challenges]

NEXT_STEPS:
[3-5 concrete next steps to develop this idea]

Be concise and actionable. Focus on practical assessment."""

        return prompt

    def _parse_idea_analysis(self, response: str) -> Dict[str, Any]:
        """Parse Claude's response into structured data"""

        analysis = {
            "category": "uncategorized",
            "potential": 5,
            "tags": [],
            "required_skills": [],
            "monetization": "none",
            "effort": "medium",
            "analysis_text": "",
            "next_steps": []
        }

        lines = response.strip().split('\n')
        current_section = None

        for line in lines:
            line = line.strip()

            if line.startswith("CATEGORY:"):
                analysis["category"] = line.split(":", 1)[1].strip().lower()

            elif line.startswith("POTENTIAL:"):
                try:
                    potential_text = line.split(":", 1)[1].strip()
                    # Extract number (might be "8/10" or just "8")
                    potential_num = ''.join(filter(str.isdigit, potential_text.split()[0]))
                    analysis["potential"] = int(potential_num) if potential_num else 5
                except:
                    analysis["potential"] = 5

            elif line.startswith("TAGS:"):
                tags_text = line.split(":", 1)[1].strip()
                analysis["tags"] = [t.strip() for t in tags_text.split(',') if t.strip()]

            elif line.startswith("REQUIRED_SKILLS:"):
                skills_text = line.split(":", 1)[1].strip()
                analysis["required_skills"] = [s.strip() for s in skills_text.split(',') if s.strip()]

            elif line.startswith("MONETIZATION:"):
                monetization = line.split(":", 1)[1].strip().lower()
                if monetization in ["direct", "indirect", "none"]:
                    analysis["monetization"] = monetization

            elif line.startswith("EFFORT:"):
                effort = line.split(":", 1)[1].strip().lower()
                if effort in ["low", "medium", "high"]:
                    analysis["effort"] = effort

            elif line.startswith("ANALYSIS:"):
                current_section = "analysis"
                continue

            elif line.startswith("NEXT_STEPS:"):
                current_section = "next_steps"
                continue

            elif current_section == "analysis" and line:
                analysis["analysis_text"] += line + " "

            elif current_section == "next_steps" and line:
                # Clean up list markers
                step = line.lstrip('- ').lstrip('* ').lstrip('1234567890. ')
                if step:
                    analysis["next_steps"].append(step)

        # Clean up analysis text
        analysis["analysis_text"] = analysis["analysis_text"].strip()

        return analysis

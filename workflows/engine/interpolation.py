"""
Workflow Engine - Interpolation Engine

Handles {{variable}} replacement and condition evaluation.
"""

import operator
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from workflows.engine.exceptions import (
    InterpolationError,
    ConditionEvaluationError,
)


# ═══════════════════════════════════════════════════════════════
# INTERPOLATOR CLASS
# ═══════════════════════════════════════════════════════════════

class Interpolator:
    """
    Handles variable interpolation in templates and conditions.

    Supports:
    - {{variable}} - Simple variable replacement
    - {{step.field}} - Nested access to step results
    - {{step.nested.field}} - Deep nested access
    - {{date}} - Current date (YYYY-MM-DD)
    - {{timestamp}} - Current timestamp
    - {{workflow}} - Workflow name
    """

    PATTERN = re.compile(r'\{\{([^}]+)\}\}')

    # Built-in variables
    BUILTINS = {
        "date": lambda: datetime.now().strftime("%Y-%m-%d"),
        "timestamp": lambda: datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
        "time": lambda: datetime.now().strftime("%H:%M:%S"),
        "year": lambda: datetime.now().strftime("%Y"),
        "month": lambda: datetime.now().strftime("%m"),
        "day": lambda: datetime.now().strftime("%d"),
    }

    def __init__(self, context: Dict[str, Any] = None):
        """
        Initialize with a context dictionary.

        Args:
            context: Dict containing variables and step results
        """
        self.context = context or {}

    def set_context(self, context: Dict[str, Any]):
        """Update the context dictionary."""
        self.context = context

    def add_to_context(self, key: str, value: Any):
        """Add a single value to context."""
        self.context[key] = value

    def interpolate(self, template: str) -> str:
        """
        Replace all {{variable}} patterns in template.

        Args:
            template: String containing {{variable}} patterns

        Returns:
            String with all variables replaced

        Raises:
            InterpolationError: If a variable cannot be resolved
        """
        if not template or "{{" not in template:
            return template

        def replacer(match):
            expression = match.group(1).strip()
            try:
                value = self._resolve(expression)
                return self._stringify(value)
            except Exception as e:
                raise InterpolationError(expression, str(e))

        return self.PATTERN.sub(replacer, template)

    def _resolve(self, expression: str) -> Any:
        """
        Resolve a single expression to its value.

        Args:
            expression: The expression without {{ }}

        Returns:
            The resolved value
        """
        # Check builtins first
        if expression in self.BUILTINS:
            return self.BUILTINS[expression]()

        # Check if it's a simple variable
        if expression in self.context:
            return self.context[expression]

        # Handle nested access (e.g., step.field.nested)
        if "." in expression:
            return self._resolve_nested(expression)

        # Not found
        raise KeyError(f"Variable '{expression}' not found in context")

    def _resolve_nested(self, expression: str) -> Any:
        """
        Resolve nested access like step.field.nested.

        Args:
            expression: Dot-separated path

        Returns:
            The resolved value
        """
        parts = expression.split(".")
        current = self.context

        for i, part in enumerate(parts):
            if isinstance(current, dict):
                if part not in current:
                    path = ".".join(parts[:i+1])
                    raise KeyError(f"Key '{part}' not found at '{path}'")
                current = current[part]
            elif hasattr(current, part):
                current = getattr(current, part)
            elif hasattr(current, '__getitem__'):
                try:
                    # Try numeric index
                    if part.isdigit():
                        current = current[int(part)]
                    else:
                        current = current[part]
                except (KeyError, IndexError, TypeError):
                    path = ".".join(parts[:i+1])
                    raise KeyError(f"Cannot access '{part}' at '{path}'")
            else:
                path = ".".join(parts[:i+1])
                raise KeyError(f"Cannot access '{part}' at '{path}'")

        return current

    def _stringify(self, value: Any) -> str:
        """Convert a value to string for template replacement."""
        if value is None:
            return ""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, (list, dict)):
            import json
            return json.dumps(value, ensure_ascii=False, indent=2)
        return str(value)

    def resolve_path(self, path_template: str) -> Path:
        """
        Resolve a path template.

        Args:
            path_template: Path with {{variable}} patterns

        Returns:
            Resolved Path object
        """
        resolved = self.interpolate(path_template)
        return Path(resolved)

    def evaluate_condition(self, condition: str) -> bool:
        """
        Evaluate a condition expression.

        Supports:
        - {{count}} > 0
        - {{status}} == 'active'
        - {{items}} != '[]'
        - {{flag}} == true

        Args:
            condition: Condition string

        Returns:
            Boolean result

        Raises:
            ConditionEvaluationError: If condition cannot be evaluated
        """
        if not condition:
            return True

        try:
            # First interpolate all variables
            interpolated = self.interpolate(condition)

            # Parse and evaluate
            return self._evaluate_expression(interpolated)

        except InterpolationError:
            raise
        except Exception as e:
            raise ConditionEvaluationError(condition, str(e))

    def _evaluate_expression(self, expression: str) -> bool:
        """
        Safely evaluate a comparison expression.

        Args:
            expression: Interpolated expression like "5 > 0"

        Returns:
            Boolean result
        """
        expression = expression.strip()

        # Handle boolean literals
        if expression.lower() == "true":
            return True
        if expression.lower() == "false":
            return False

        # Define operators
        ops = {
            "==": operator.eq,
            "!=": operator.ne,
            ">=": operator.ge,
            "<=": operator.le,
            ">": operator.gt,
            "<": operator.lt,
        }

        # Find and apply operator (check longer operators first)
        for op_str, op_func in sorted(ops.items(), key=lambda x: -len(x[0])):
            if op_str in expression:
                parts = expression.split(op_str, 1)
                if len(parts) == 2:
                    left = self._parse_value(parts[0].strip())
                    right = self._parse_value(parts[1].strip())
                    return op_func(left, right)

        # If no operator found, treat as truthy check
        return bool(self._parse_value(expression))

    def _parse_value(self, value_str: str) -> Any:
        """
        Parse a string value to its Python type.

        Args:
            value_str: String representation of value

        Returns:
            Parsed value (int, float, bool, str, or None)
        """
        value_str = value_str.strip()

        # Remove quotes
        if (value_str.startswith("'") and value_str.endswith("'")) or \
           (value_str.startswith('"') and value_str.endswith('"')):
            return value_str[1:-1]

        # Boolean
        if value_str.lower() == "true":
            return True
        if value_str.lower() == "false":
            return False

        # None/null
        if value_str.lower() in ("none", "null", ""):
            return None

        # Number
        try:
            if "." in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            pass

        # List/Dict (JSON)
        if value_str.startswith("[") or value_str.startswith("{"):
            import json
            try:
                return json.loads(value_str)
            except json.JSONDecodeError:
                pass

        # Default to string
        return value_str


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def interpolate(template: str, context: Dict[str, Any]) -> str:
    """
    Convenience function for one-off interpolation.

    Args:
        template: String with {{variable}} patterns
        context: Variable context

    Returns:
        Interpolated string
    """
    return Interpolator(context).interpolate(template)


def evaluate_condition(condition: str, context: Dict[str, Any]) -> bool:
    """
    Convenience function for one-off condition evaluation.

    Args:
        condition: Condition string
        context: Variable context

    Returns:
        Boolean result
    """
    return Interpolator(context).evaluate_condition(condition)

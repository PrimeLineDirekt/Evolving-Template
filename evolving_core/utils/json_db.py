"""
JSON Database Utilities

Provides safe JSON read/write operations with validation.
"""

import json
from pathlib import Path
from typing import Any, List, Dict, Optional
from .file_ops import FileOps


class JSONDatabase:
    """JSON file-based database operations"""

    def __init__(self, base_path: Path):
        """
        Initialize JSON database.

        Args:
            base_path: Root directory for database files
        """
        self.file_ops = FileOps(base_path)
        self.base_path = base_path

    def read_json(self, relative_path: str, default: Any = None) -> Any:
        """
        Read JSON file.

        Args:
            relative_path: Path relative to base_path
            default: Default value if file doesn't exist

        Returns:
            Parsed JSON data or default value
        """
        try:
            content = self.file_ops.read_file(relative_path)
            return json.loads(content)
        except FileNotFoundError:
            return default if default is not None else {}
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {relative_path}: {e}")

    def write_json(self, relative_path: str, data: Any, backup: bool = True, indent: int = 2) -> None:
        """
        Write JSON file atomically.

        Args:
            relative_path: Path relative to base_path
            data: Data to serialize as JSON
            backup: Create backup before writing
            indent: JSON indentation (default: 2)
        """
        content = json.dumps(data, indent=indent, ensure_ascii=False)
        self.file_ops.write_file(relative_path, content, backup=backup)

    def read_index(self, relative_path: str) -> List[Dict[str, Any]]:
        """
        Read index JSON file (returns empty list if not found).

        Args:
            relative_path: Path relative to base_path

        Returns:
            List of items from index
        """
        return self.read_json(relative_path, default=[])

    def write_index(self, relative_path: str, items: List[Dict[str, Any]]) -> None:
        """
        Write index JSON file.

        Args:
            relative_path: Path relative to base_path
            items: List of items to write
        """
        self.write_json(relative_path, items, backup=True)

    def append_to_index(self, relative_path: str, item: Dict[str, Any]) -> None:
        """
        Append item to index file.

        Args:
            relative_path: Path relative to base_path
            item: Item to append
        """
        items = self.read_index(relative_path)
        items.append(item)
        self.write_index(relative_path, items)

    def update_in_index(self, relative_path: str, item_id: str, updates: Dict[str, Any], id_field: str = "id") -> bool:
        """
        Update item in index by ID.

        Args:
            relative_path: Path relative to base_path
            item_id: ID of item to update
            updates: Fields to update
            id_field: Name of ID field (default: "id")

        Returns:
            True if item was found and updated, False otherwise
        """
        items = self.read_index(relative_path)
        updated = False

        for item in items:
            if item.get(id_field) == item_id:
                item.update(updates)
                updated = True
                break

        if updated:
            self.write_index(relative_path, items)

        return updated

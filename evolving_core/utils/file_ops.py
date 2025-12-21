"""
File Operations Utilities

Provides safe, atomic file operations with backup support.
"""

import json
import shutil
from pathlib import Path
from typing import Any, Optional
from datetime import datetime


class FileOps:
    """Safe file operations with backup support"""

    def __init__(self, base_path: Path):
        """
        Initialize FileOps with base path.

        Args:
            base_path: Root directory for all operations
        """
        self.base_path = Path(base_path)

    def read_file(self, relative_path: str) -> str:
        """
        Read text file.

        Args:
            relative_path: Path relative to base_path

        Returns:
            File contents as string

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path = self.base_path / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        return file_path.read_text(encoding='utf-8')

    def write_file(self, relative_path: str, content: str, backup: bool = True) -> None:
        """
        Write text file atomically with optional backup.

        Args:
            relative_path: Path relative to base_path
            content: Content to write
            backup: Create backup before writing (default: True)
        """
        file_path = self.base_path / relative_path

        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Backup existing file if requested
        if backup and file_path.exists():
            self._create_backup(file_path)

        # Atomic write: write to temp file, then rename
        temp_path = file_path.with_suffix('.tmp')
        temp_path.write_text(content, encoding='utf-8')
        temp_path.replace(file_path)

    def file_exists(self, relative_path: str) -> bool:
        """Check if file exists"""
        return (self.base_path / relative_path).exists()

    def ensure_dir(self, relative_path: str) -> Path:
        """
        Ensure directory exists.

        Args:
            relative_path: Path relative to base_path

        Returns:
            Created directory path
        """
        dir_path = self.base_path / relative_path
        dir_path.mkdir(parents=True, exist_ok=True)
        return dir_path

    def _create_backup(self, file_path: Path) -> None:
        """Create timestamped backup of file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = file_path.with_suffix(f'.backup_{timestamp}{file_path.suffix}')
        shutil.copy2(file_path, backup_path)

#!/usr/bin/env python3
"""
Pre-commit script to sync notebooks from solutions to exercises directory.

This script copies all notebooks from the solutions/ directory to the exercises/ directory,
removing cell outputs to create clean exercise versions for students.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, List


class NotebookSyncer:
    """Handles synchronization of notebooks between solutions and exercises directories."""

    def __init__(
        self, solutions_dir: str = "solutions", exercises_dir: str = "exercises"
    ):
        """
        Initialize the NotebookSyncer.

        Args:
            solutions_dir: Path to the solutions directory
            exercises_dir: Path to the exercises directory
        """
        self.solutions_dir = Path(solutions_dir)
        self.exercises_dir = Path(exercises_dir)
        self.logger = self._setup_logging()

        # Ensure directories exist
        self.solutions_dir.mkdir(exist_ok=True)
        self.exercises_dir.mkdir(exist_ok=True)

    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        return logging.getLogger(__name__)

    def find_notebooks(self, directory: Path) -> List[Path]:
        """
        Find all .ipynb files in the given directory.

        Args:
            directory: Directory to search for notebooks

        Returns:
            List of notebook file paths
        """
        return list(directory.glob("*.ipynb"))

    def remove_cell_outputs(self, notebook_data: Dict) -> Dict:
        """
        Remove cell outputs from notebook data.

        Args:
            notebook_data: The notebook JSON data

        Returns:
            Notebook data with cell outputs removed
        """
        cleaned_notebook = notebook_data.copy()

        # Remove outputs from all cells
        for cell in cleaned_notebook.get("cells", []):
            if "outputs" in cell:
                cell["outputs"] = []
            if "execution_count" in cell:
                cell["execution_count"] = None

        # Clear metadata that might contain execution info
        if "metadata" in cleaned_notebook:
            metadata = cleaned_notebook["metadata"]
            # Keep essential metadata but remove execution-related info
            execution_keys = ["execution", "execution_count", "last_execution"]
            for key in execution_keys:
                if key in metadata:
                    del metadata[key]

        return cleaned_notebook

    def copy_notebook_without_outputs(self, source_path: Path, dest_path: Path) -> bool:
        """
        Copy a notebook file, removing cell outputs in the process.

        Args:
            source_path: Path to source notebook
            dest_path: Path to destination notebook

        Returns:
            True if successful, False otherwise
        """
        try:
            # Read the source notebook
            with open(source_path, "r", encoding="utf-8") as f:
                notebook_data = json.load(f)

            # Remove cell outputs
            cleaned_notebook = self.remove_cell_outputs(notebook_data)

            # Write the cleaned notebook to destination
            with open(dest_path, "w", encoding="utf-8") as f:
                json.dump(cleaned_notebook, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Successfully copied {source_path} -> {dest_path}")
            return True

        except Exception as e:
            self.logger.error(f"Error copying {source_path}: {e}")
            return False

    def sync_notebooks(self) -> bool:
        """
        Sync all notebooks from solutions to exercises directory.

        Returns:
            True if all operations successful, False otherwise
        """
        self.logger.info("Starting notebook synchronization...")

        # Find all notebooks in solutions directory
        solution_notebooks = self.find_notebooks(self.solutions_dir)

        if not solution_notebooks:
            self.logger.warning(f"No notebooks found in {self.solutions_dir}")
            return True

        self.logger.info(
            f"Found {len(solution_notebooks)} notebooks in solutions directory"
        )

        success_count = 0
        total_count = len(solution_notebooks)

        for notebook_path in solution_notebooks:
            # Create destination path
            dest_path = self.exercises_dir / notebook_path.name

            # Copy notebook without outputs
            if self.copy_notebook_without_outputs(notebook_path, dest_path):
                success_count += 1

        self.logger.info(
            f"Sync completed: {success_count}/{total_count} notebooks processed successfully"
        )

        return success_count == total_count


def main() -> int:
    """
    Main entry point for the notebook sync script.

    Returns:
        0 on success, 1 on failure
    """
    try:
        syncer = NotebookSyncer()
        success = syncer.sync_notebooks()
        return 0 if success else 1

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
Pre-commit script to sync notebooks from solutions to exercises directory.

This script copies all notebooks from the solutions/ directory to the exercises/ directory,
removing cell outputs only from cells within "### To Complete ###" and "### End of To Complete ###"
markers to create clean exercise versions for students while preserving other outputs.
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

    def validate_markers(self, notebook_data: Dict) -> bool:
        """
        Validate that "To Complete" markers are properly paired.

        Args:
            notebook_data: The notebook JSON data

        Returns:
            True if markers are properly paired, False otherwise
        """
        cells = notebook_data.get("cells", [])

        if not isinstance(cells, list):
            self.logger.warning("Invalid notebook structure: cells is not a list")
            return False

        start_markers = 0
        end_markers = 0

        for i, cell in enumerate(cells):
            try:
                # Ensure cell is a dictionary
                if not isinstance(cell, dict):
                    continue

                source_text = ""
                if "source" in cell:
                    if isinstance(cell["source"], list):
                        source_text = "".join(str(item) for item in cell["source"])
                    elif isinstance(cell["source"], str):
                        source_text = cell["source"]
                    else:
                        source_text = str(cell["source"])

                if "### To Complete ###" in source_text:
                    start_markers += 1
                if "### End of To Complete ###" in source_text:
                    end_markers += 1

            except Exception as e:
                self.logger.warning(f"Error validating cell {i}: {e}")
                continue

        if start_markers != end_markers:
            self.logger.warning(f"Marker mismatch: {start_markers} start markers, {end_markers} end markers")
            return False

        return True

    def debug_markers(self, notebook_data: Dict) -> None:
        """
        Debug method to count and display all markers found in a notebook.

        Args:
            notebook_data: The notebook JSON data
        """
        cells = notebook_data.get("cells", [])
        start_markers = []
        end_markers = []

        for i, cell in enumerate(cells):
            try:
                if not isinstance(cell, dict):
                    continue

                source_text = ""
                if "source" in cell:
                    if isinstance(cell["source"], list):
                        source_text = "".join(str(item) for item in cell["source"])
                    elif isinstance(cell["source"], str):
                        source_text = cell["source"]
                    else:
                        source_text = str(cell["source"])

                if "### To Complete ###" in source_text:
                    start_markers.append((i, source_text.strip()))
                if "### End of To Complete ###" in source_text:
                    end_markers.append((i, source_text.strip()))

            except Exception as e:
                continue

        self.logger.info(f"Found {len(start_markers)} start markers and {len(end_markers)} end markers")

        if start_markers:
            self.logger.info("Start markers:")
            for idx, text in start_markers[:3]:  # Show first 3
                self.logger.info(f"  Cell {idx}: {repr(text)}")

        if end_markers:
            self.logger.info("End markers:")
            for idx, text in end_markers[:3]:  # Show first 3
                self.logger.info(f"  Cell {idx}: {repr(text)}")

    def remove_cell_outputs(self, notebook_data: Dict) -> Dict:
        """
        Remove cell outputs from notebook data, with special handling for "To Complete" sections.

        Args:
            notebook_data: The notebook JSON data

        Returns:
            Notebook data with cell outputs removed for "To Complete" sections only
        """
        cleaned_notebook = notebook_data.copy()
        cells = cleaned_notebook.get("cells", [])

        if not isinstance(cells, list):
            self.logger.warning("Invalid notebook structure: cells is not a list")
            return cleaned_notebook

        # Track whether we're currently in a "To Complete" section
        in_to_complete_section = False
        section_count = 0

        for i, cell in enumerate(cells):
            try:
                # Ensure cell is a dictionary
                if not isinstance(cell, dict):
                    self.logger.warning(f"Cell {i} is not a dictionary, skipping")
                    continue

                # Extract source text from different possible cell structures
                source_text = ""
                if "source" in cell:
                    if isinstance(cell["source"], list):
                        source_text = "".join(str(item) for item in cell["source"])
                    elif isinstance(cell["source"], str):
                        source_text = cell["source"]
                    else:
                        source_text = str(cell["source"])

                # Check if this cell contains both markers (self-contained section)
                has_start = "### To Complete ###" in source_text
                has_end = "### End of To Complete ###" in source_text

                if has_start and has_end:
                    # Self-contained section - clear outputs from this cell
                    section_count += 1
                    self.logger.debug(f"Found self-contained 'To Complete' section in cell {i}")
                    if "outputs" in cell:
                        cell["outputs"] = []
                    if "execution_count" in cell:
                        cell["execution_count"] = None
                    continue

                # Check if this cell contains the start marker
                if has_start:
                    in_to_complete_section = True
                    section_count += 1
                    self.logger.debug(f"Found 'To Complete' marker in cell {i}")
                    # Clear outputs from the marker cell itself
                    if "outputs" in cell:
                        cell["outputs"] = []
                    if "execution_count" in cell:
                        cell["execution_count"] = None
                    continue

                # Check if this cell contains the end marker
                if has_end:
                    in_to_complete_section = False
                    self.logger.debug(f"Found 'End of To Complete' marker in cell {i}")
                    # Clear outputs from the marker cell itself
                    if "outputs" in cell:
                        cell["outputs"] = []
                    if "execution_count" in cell:
                        cell["execution_count"] = None
                    continue

                # Only clear outputs if we're in a "To Complete" section
                if in_to_complete_section:
                    if "outputs" in cell:
                        cell["outputs"] = []
                    if "execution_count" in cell:
                        cell["execution_count"] = None

            except Exception as e:
                self.logger.warning(f"Error processing cell {i}: {e}")
                continue

        # Clear metadata that might contain execution info
        if "metadata" in cleaned_notebook:
            metadata = cleaned_notebook["metadata"]
            # Keep essential metadata but remove execution-related info
            execution_keys = ["execution", "execution_count", "last_execution"]
            for key in execution_keys:
                if key in metadata:
                    del metadata[key]

        self.logger.info(f"Processed {section_count} 'To Complete' sections")
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

            # Debug markers first
            self.debug_markers(notebook_data)

            # Validate markers first
            if not self.validate_markers(notebook_data):
                self.logger.warning(f"Marker validation failed for {source_path}")

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

    def test_single_notebook(self, notebook_name: str) -> bool:
        """
        Test the script on a single notebook for debugging purposes.

        Args:
            notebook_name: Name of the notebook to test

        Returns:
            True if successful, False otherwise
        """
        source_path = self.solutions_dir / notebook_name
        if not source_path.exists():
            self.logger.error(f"Notebook {notebook_name} not found in solutions directory")
            return False

        self.logger.info(f"Testing single notebook: {notebook_name}")
        return self.copy_notebook_without_outputs(source_path, self.exercises_dir / notebook_name)

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
            self.logger.info(f"Processing {notebook_path.name}...")

            # Create destination path
            dest_path = self.exercises_dir / notebook_path.name

            # Copy notebook without outputs
            if self.copy_notebook_without_outputs(notebook_path, dest_path):
                success_count += 1
                self.logger.info(f"✓ Successfully processed {notebook_path.name}")
            else:
                self.logger.error(f"✗ Failed to process {notebook_path.name}")

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

        # Check if a specific notebook was requested for testing
        if len(sys.argv) > 1:
            notebook_name = sys.argv[1]
            if not notebook_name.endswith('.ipynb'):
                notebook_name += '.ipynb'
            success = syncer.test_single_notebook(notebook_name)
        else:
            success = syncer.sync_notebooks()

        return 0 if success else 1

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

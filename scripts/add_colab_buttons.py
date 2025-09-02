#!/usr/bin/env python3
"""
Script to add Google Colab buttons and installation setup to all Jupyter notebooks.
This script will add a Colab button at the top of each notebook that opens it in Google Colab,
along with installation cells for git and required packages.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Tuple


class ColabButtonAdder:
    """Adds Google Colab buttons and installation setup to Jupyter notebooks."""

    def __init__(
        self,
        base_url: str = "https://colab.research.google.com/github/PrunaAI/ai-efficiency-courses/blob/main/",
    ):
        """
        Initialize the Colab button adder.

        Args:
            base_url: The base URL for Google Colab with the repository path
        """
        self.base_url = base_url

    def validate_notebook_structure(self, notebook: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate that the notebook has the required structure for safe updates.

        Args:
            notebook: The notebook dictionary to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Check if it's a valid notebook structure
            if not isinstance(notebook, dict):
                return False, "Notebook is not a valid dictionary"

            # Check for required top-level keys
            required_keys = ["cells", "metadata", "nbformat", "nbformat_minor"]
            missing_keys = [key for key in required_keys if key not in notebook]
            if missing_keys:
                return False, f"Missing required notebook keys: {missing_keys}"

            # Validate cells structure
            cells = notebook.get("cells", [])
            if not isinstance(cells, list):
                return False, "Cells must be a list"

            # Validate each cell has required structure
            for i, cell in enumerate(cells):
                if not isinstance(cell, dict):
                    return False, f"Cell {i} is not a valid dictionary"

                if "cell_type" not in cell:
                    return False, f"Cell {i} missing cell_type"

                if cell["cell_type"] not in ["code", "markdown", "raw"]:
                    return False, f"Cell {i} has invalid cell_type: {cell['cell_type']}"

            return True, ""

        except Exception as e:
            return False, f"Validation error: {str(e)}"

    def can_update_cells(self, notebook_path: str) -> Tuple[bool, str]:
        """
        Check if the notebook can be safely updated.

        Args:
            notebook_path: Path to the notebook file

        Returns:
            Tuple of (can_update, reason)
        """
        try:
            # Check if file exists and is readable
            if not os.path.exists(notebook_path):
                return False, f"File does not exist: {notebook_path}"

            if not os.access(notebook_path, os.R_OK):
                return False, f"Cannot read file: {notebook_path}"

            if not os.access(notebook_path, os.W_OK):
                return False, f"Cannot write to file: {notebook_path}"

            # Try to read and parse the notebook
            with open(notebook_path, "r", encoding="utf-8") as f:
                notebook = json.load(f)

            # Validate notebook structure
            is_valid, error_msg = self.validate_notebook_structure(notebook)
            if not is_valid:
                return False, f"Invalid notebook structure: {error_msg}"

            return True, "Notebook can be updated"

        except json.JSONDecodeError as e:
            return False, f"Invalid JSON in notebook: {e}"
        except Exception as e:
            return False, f"Error checking notebook: {e}"

    def create_git_installation_cell(self) -> Dict[str, Any]:
        """
        Create a code cell for installing the project directly from git.

        Returns:
            Dictionary representing the git installation cell
        """
        install_code = """# Install the project directly from git repository
!uv pip install git+https://github.com/PrunaAI/ai-efficiency-courses.git"""

        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [install_code],
        }

    def create_colab_button_cell(self, notebook_path: str) -> Dict[str, Any]:
        """
        Create a markdown cell with a Google Colab button and setup instructions.

        Args:
            notebook_path: Path to the notebook file

        Returns:
            Dictionary representing the markdown cell
        """
        # Convert path to GitHub-style path
        github_path = str(Path(notebook_path)).replace("\\", "/")

        colab_url = f"{self.base_url}{github_path}"

        button_html = f"""
<div align="center">
  <a href="{colab_url}" target="_parent">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
  </a>
</div>

---
**💡 Tip**: Click the button above to open this notebook in Google Colab for free GPU access!

## Installation

This notebook includes automatic setup cells that will install the project from git repository with UV.

**Note**: Run the setup cells below before starting the exercises.
        """.strip()

        return {"cell_type": "markdown", "metadata": {}, "source": [button_html]}

    def find_existing_cells(
        self, cells: List[Dict[str, Any]]
    ) -> Tuple[bool, bool, bool]:
        """
        Find existing Colab button and setup cells and check if they're up-to-date.

        Args:
            cells: List of notebook cells

        Returns:
            Tuple of (has_button, has_setup, both_up_to_date)
        """
        has_button = False
        has_setup = False
        button_up_to_date = False
        setup_up_to_date = False

        # Check for Colab button
        for cell in cells:
            if cell.get("cell_type") == "markdown" and "colab-badge.svg" in str(
                cell.get("source", [])
            ):
                has_button = True
                # Check if button is up-to-date by looking for the correct URL pattern
                cell_source = "".join(cell.get("source", []))
                if (
                    "colab.research.google.com/github/PrunaAI/ai-efficiency-courses"
                    in cell_source
                ):
                    button_up_to_date = True
                break

        # Check for setup cell
        desired_git_cell = self.create_git_installation_cell()
        desired_source = "".join(desired_git_cell.get("source", [])).strip()

        for cell in cells:
            if cell.get("cell_type") == "code":
                cell_source = "".join(cell.get("source", [])).strip()
                if (
                    "!uv pip install git+https://github.com/PrunaAI/ai-efficiency-courses.git"
                    in cell_source
                ):
                    has_setup = True
                    if cell_source == desired_source:
                        setup_up_to_date = True
                    break

        both_up_to_date = button_up_to_date and setup_up_to_date
        return has_button, has_setup, both_up_to_date

    def remove_existing_cells(
        self, cells: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Remove any existing Colab button and setup cells from the notebook.

        Args:
            cells: List of notebook cells

        Returns:
            Updated list of cells with existing button/setup cells removed
        """
        filtered_cells = []

        for cell in cells:
            # Skip Colab button cells
            if cell.get("cell_type") == "markdown" and "colab-badge.svg" in str(
                cell.get("source", [])
            ):
                continue

            # Skip setup cells
            if cell.get("cell_type") == "code":
                cell_source = "".join(cell.get("source", [])).strip()
                if (
                    "!uv pip install git+https://github.com/PrunaAI/ai-efficiency-courses.git"
                    in cell_source
                ):
                    continue

            # Keep all other cells
            filtered_cells.append(cell)

        return filtered_cells

    def update_notebook_cells(self, notebook_path: str) -> bool:
        """
        Update notebook with Colab button and setup cells in a single operation.

        Args:
            notebook_path: Path to the notebook file

        Returns:
            True if successful, False otherwise
        """
        try:
            can_update, reason = self.can_update_cells(notebook_path)
            if not can_update:
                print(f"❌ Cannot update {notebook_path}: {reason}")
                return False

            with open(notebook_path, "r", encoding="utf-8") as f:
                notebook = json.load(f)

            is_valid, error_msg = self.validate_notebook_structure(notebook)
            if not is_valid:
                print(f"❌ Invalid notebook structure in {notebook_path}: {error_msg}")
                return False

            cells = notebook.get("cells", [])
            has_button, has_setup, both_up_to_date = self.find_existing_cells(cells)

            if both_up_to_date:
                print(
                    f"✅ Both Colab button and setup cell are already up-to-date in {notebook_path}"
                )
                return True

            # Remove any existing button/setup cells and add fresh ones
            cells = self.remove_existing_cells(cells)
            button_cell = self.create_colab_button_cell(notebook_path)
            setup_cell = self.create_git_installation_cell()
            cells.insert(0, button_cell)
            cells.insert(1, setup_cell)
            notebook["cells"] = cells

            try:
                with open(notebook_path, "w", encoding="utf-8") as f:
                    json.dump(notebook, f, indent=2, ensure_ascii=False)
                print(f"💾 Updated {notebook_path} with Colab button and setup cell.")
                return True
            except Exception as e:
                print(f"❌ Failed to write updated notebook {notebook_path}: {e}")
                return False

        except Exception as e:
            print(f"❌ Error processing {notebook_path}: {e}")
            return False

    def process_directory(self, directory_path: str) -> Dict[str, int]:
        """
        Process all notebooks in a directory.

        Args:
            directory_path: Path to the directory containing notebooks

        Returns:
            Dictionary with success and failure counts
        """
        results = {"success": 0, "failed": 0}

        if not os.path.exists(directory_path):
            print(f"❌ Directory not found: {directory_path}")
            return results

        notebook_files = list(Path(directory_path).glob("*.ipynb"))
        if not notebook_files:
            print(f"ℹ️  No notebook files found in {directory_path}")
            return results

        print(f"📁 Found {len(notebook_files)} notebook(s) in {directory_path}")

        for file_path in notebook_files:
            print(f"\n📝 Processing: {file_path}")
            if self.update_notebook_cells(str(file_path)):
                results["success"] += 1
            else:
                results["failed"] += 1

        return results


def main():
    """Main function to add Colab buttons and setup cells to all notebooks."""
    print("🚀 Adding Google Colab buttons and setup cells to all notebooks...")

    # Initialize the adder
    adder = ColabButtonAdder()

    # Process exercises directory
    print("\n📁 Processing exercises directory...")
    exercises_results = adder.process_directory("exercises")

    # Process solutions directory
    print("\n📁 Processing solutions directory...")
    solutions_results = adder.process_directory("solutions")

    # Print summary
    print("\n📊 Summary:")
    print(
        f"Exercises: {exercises_results['success']} successful, {exercises_results['failed']} failed"
    )
    print(
        f"Solutions: {solutions_results['success']} successful, {solutions_results['failed']} failed"
    )

    total_success = exercises_results["success"] + solutions_results["success"]
    total_failed = exercises_results["failed"] + solutions_results["failed"]

    print(f"\n🎉 Total: {total_success} notebooks updated successfully!")
    if total_failed > 0:
        print(f"⚠️  {total_failed} notebooks failed to update")


if __name__ == "__main__":
    main()

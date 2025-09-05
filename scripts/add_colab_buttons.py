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
        utility_cells: List[Tuple[str, str]] = None,
    ):
        """
        Initialize the Colab button adder.

        Args:
            base_url: The base URL for Google Colab with the repository path
            utility_cells: List of tuples with (cell_type, content) for utility cells
        """
        self.base_url = base_url
        # Default utility cells if none provided
        if utility_cells is None:
            self.utility_cells = [
                (
                    "code",
                    "\n".join(
                        [
                            "# Install project directly from git repository",
                            "!uv pip install git+https://github.com/PrunaAI/ai-efficiency-courses.git",
                        ]
                    ),
                ),
                (
                    "markdown",
                    "\n".join(
                        [
                            "## Utility cells",
                            "",
                            "During the course, we'll leverage some course utilities to streamline our workflow. These utilities are located in the `course` package, which can simply be imported given that we installed the project from git repository above.",
                            "You can find the source code [here](https://github.com/PrunaAI/ai-efficiency-courses/tree/main/course).",
                            "",
                            "These utilities will help us:",
                            "- Load and manage lists of model ids that we have verified to work.",
                            "- Generate informative plots for model analysis.",
                            "- Iterate efficiently over evaluation and model configuration options.",
                            "",
                            "Let's first load our models. We will use `SMALL_MODEL_IDS`, which are sub 1B parameters which should be easy to download and load into memory. We recommend starting with these smaller models but feel free to experiment with other models until you reach your GPU memory limit!",
                        ]
                    ),
                ),
                (
                    "code",
                    "\n".join(
                        [
                            "from course import SMALL_MODEL_IDS, MEDIUM_MODEL_IDS, LARGE_MODEL_IDS, ALL_MODEL_IDS",
                            "",
                            "MODEL_IDS = SMALL_MODEL_IDS",
                            "# MODEL_IDS = MEDIUM_MODEL_IDS",
                            "# MODEL_IDS = LARGE_MODEL_IDS",
                            "# MODEL_IDS = ALL_MODEL_IDS",
                            "",
                            "MODEL_IDS",
                        ]
                    ),
                ),
                (
                    "markdown",
                    "\n".join(
                        [
                            "We also recommend to set a custom cache directory for models. Loading models can take significant disk space. To avoid filling up your default disk, we recommend setting a custom cache directory for downloaded models. You can do this by running the following in a terminal or in a notebook cell:"
                        ]
                    ),
                ),
                (
                    "code",
                    "\n".join(
                        [
                            "# Replace <path_to_cache> with your desired cache path",
                            "import os",
                            "",
                            'CACHE_PATH = "<path_to_cache>"',
                            'os.environ["TORCH_HOME"] = CACHE_PATH',
                            'os.environ["HF_HOME"] = CACHE_PATH',
                            'os.environ["HUGGINGFACE_HUB_CACHE"] = CACHE_PATH',
                            'os.environ["HUGGINGFACE_ASSETS_CACHE"] = CACHE_PATH',
                            'os.environ["TRANSFORMERS_CACHE"] = CACHE_PATH',
                        ]
                    ),
                ),
                (
                    "markdown",
                    "\n".join(
                        ["You can also clear the cache by running the following cell:"]
                    ),
                ),
                (
                    "code",
                    "\n".join(
                        [
                            "from course.models import clear_cache",
                            "",
                            'clear_cache("<path_to_cache>")',
                        ]
                    ),
                ),
            ]
        else:
            self.utility_cells = utility_cells

    def update_utility_cells(self, new_utility_cells: List[Tuple[str, str]]) -> None:
        """
        Update the utility cells configuration.

        Args:
            new_utility_cells: New list of tuples with (cell_type, content)
        """
        self.utility_cells = new_utility_cells

    def get_utility_cells(self) -> List[Tuple[str, str]]:
        """
        Get the current utility cells configuration.

        Returns:
            List of tuples with (cell_type, content)
        """
        return self.utility_cells.copy()

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
        install_code = """# Install project directly from git repository
!uv pip install git+https://github.com/PrunaAI/ai-efficiency-courses.git"""

        return {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [install_code],
        }

    def create_utility_cells(
        self, utility_tuples: List[Tuple[str, str]]
    ) -> List[Dict[str, Any]]:
        """
        Create utility cells that alternate between code and markdown based on provided tuples.

        Args:
            utility_tuples: List of tuples with (cell_type, content) where cell_type is 'code' or 'markdown'

        Returns:
            List of cell dictionaries
        """
        cells = []

        for i, (cell_type, content) in enumerate(utility_tuples):
            if cell_type not in ["code", "markdown"]:
                print(
                    f"⚠️  Skipping invalid cell type '{cell_type}', must be 'code' or 'markdown'"
                )
                continue

            if cell_type == "code":
                cell = {
                    "cell_type": "code",
                    "execution_count": None,
                    "metadata": {"tags": ["utility-cell", f"utility-{i + 1}"]},
                    "outputs": [],
                    "source": [content],
                }
            else:  # markdown
                cell = {
                    "cell_type": "markdown",
                    "metadata": {"tags": ["utility-cell", f"utility-{i + 1}"]},
                    "source": [content],
                }

            cells.append(cell)

        return cells

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

        return {
            "cell_type": "markdown",
            "metadata": {"tags": ["colab-button"]},
            "source": [button_html],
        }

    def find_existing_cells(
        self, cells: List[Dict[str, Any]]
    ) -> Tuple[bool, bool, bool]:
        """
        Find existing Colab button and utility cells and check if they're up-to-date.

        Args:
            cells: List of notebook cells

        Returns:
            Tuple of (has_button, has_utilities, both_up_to_date)
        """
        has_button = False
        has_utilities = False
        button_up_to_date = False
        utilities_up_to_date = False

        # Check for Colab button
        for cell in cells:
            cell_tags = cell.get("metadata", {}).get("tags", [])
            if "colab-button" in cell_tags:
                has_button = True
                # Check if button is up-to-date by looking for the correct URL pattern
                cell_source = "".join(cell.get("source", []))
                if (
                    "colab.research.google.com/github/PrunaAI/ai-efficiency-courses"
                    in cell_source
                ):
                    button_up_to_date = True
                break

        # Check for utility cells
        desired_utility_cells = self.create_utility_cells(self.utility_cells)

        # Check if the expected utility cells exist by looking for tags and content
        expected_utility_cells = len(desired_utility_cells)

        # Count cells with utility tags
        tagged_utility_cells = 0
        for cell in cells:
            cell_tags = cell.get("metadata", {}).get("tags", [])
            if "utility-cell" in cell_tags:
                tagged_utility_cells += 1

        # Check if we have exactly the right number of tagged utility cells
        has_utilities = tagged_utility_cells == expected_utility_cells

        # For utilities to be up-to-date, we need exactly the right number
        # AND the content must match our expected content
        utilities_up_to_date = False
        if has_utilities:
            # Check if the content matches our expected utility cells
            utility_cells_found = 0
            for i, cell in enumerate(cells):
                if utility_cells_found < expected_utility_cells:
                    cell_tags = cell.get("metadata", {}).get("tags", [])
                    if "utility-cell" in cell_tags:
                        # Get the expected content for this utility cell
                        expected_content = self.utility_cells[utility_cells_found][1]
                        actual_content = "".join(cell.get("source", [])).strip()
                        if actual_content == expected_content.strip():
                            utility_cells_found += 1
                        else:
                            # Content doesn't match, so not up-to-date
                            break

            utilities_up_to_date = utility_cells_found == expected_utility_cells

        both_up_to_date = button_up_to_date and utilities_up_to_date
        return has_button, has_utilities, both_up_to_date

    def remove_existing_cells(
        self, cells: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Remove any existing Colab button and utility cells from the notebook.

        Args:
            cells: List of notebook cells

        Returns:
            Updated list of cells with existing button/utility cells removed
        """
        filtered_cells = []

        for cell in cells:
            # Skip Colab button cells
            cell_tags = cell.get("metadata", {}).get("tags", [])
            if "colab-button" in cell_tags:
                continue

            # Skip utility cells by checking for utility tags
            if "utility-cell" in cell_tags:
                continue

            # Also check for old utility cells by content similarity
            # This handles cases where old cells don't have tags
            cell_source = "".join(cell.get("source", [])).strip()
            is_old_utility = False

            # Check if this cell matches any of our expected utility cell content
            for _, expected_content in self.utility_cells:
                if cell_source == expected_content.strip():
                    is_old_utility = True
                    break

            # Also check for old cells with similar content patterns
            if not is_old_utility:
                # Check for old installation cells
                if (
                    "Install project directly from git repository" in cell_source
                    and "!uv pip install git+https://github.com/PrunaAI/ai-efficiency-courses.git"
                    in cell_source
                ):
                    is_old_utility = True
                # Check for old setup complete cells
                elif (
                    "## Setup Complete!" in cell_source
                    and "project has been installed successfully" in cell_source
                ):
                    is_old_utility = True
                # Check for old verification cells
                elif (
                    "## Installation" in cell_source
                    and "This notebook includes automatic setup cells" in cell_source
                ):
                    is_old_utility = True

            if is_old_utility:
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
            has_button, has_utilities, both_up_to_date = self.find_existing_cells(cells)

            if both_up_to_date:
                print(
                    f"✅ Both Colab button and setup cell are already up-to-date in {notebook_path}"
                )
                return True

            # Remove any existing button/utility cells and add fresh ones
            cells = self.remove_existing_cells(cells)
            button_cell = self.create_colab_button_cell(notebook_path)
            utility_cells = self.create_utility_cells(self.utility_cells)

            # Insert button cell first
            cells.insert(0, button_cell)

            # Insert utility cells after the button
            for i, utility_cell in enumerate(utility_cells):
                cells.insert(1 + i, utility_cell)

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
    """Main function to add Colab buttons and utility cells to all notebooks."""
    print("🚀 Adding Google Colab buttons and utility cells to all notebooks...")

    # Initialize the adder with default utility cells
    adder = ColabButtonAdder()

    print(f"📋 Using {len(adder.utility_cells)} utility cells:")
    for i, (cell_type, content) in enumerate(adder.utility_cells, 1):
        preview = content[:50] + "..." if len(content) > 50 else content
        print(f"  {i}. {cell_type}: {preview}")

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
